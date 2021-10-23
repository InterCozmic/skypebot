from skpy import SkypeEventLoop, SkypeNewMessageEvent
from threading import Thread
import re
from bs4 import BeautifulSoup

class ParsedArgumentsObject:
  def __init__(self, users: list, **kwargs):
    self.users = users
    for key, value in kwargs.items():
      setattr(self, key, value)

def parse_args(arg_string: str, args: list):
  soup = BeautifulSoup(arg_string, 'html.parser')
  ats = soup.find_all('at')
  users = []
  for at in ats:
    users.append((at["id"][2:], at.get_text()))
    at.decompose()
  for id in re.findall(r'\blive\:\w+', str(soup)):
    users.append((id, id[5:]))
  soup = re.sub(r'\blive\:\w+', '', str(soup))
  arg_vals = ' '.join(soup.split()).split(maxsplit=len(args)-1)
  arg = ParsedArgumentsObject(users=users)
  for key, value in dict(zip(args, arg_vals)).items():
    setattr(arg, key, value)
  return arg

class SkypePing(SkypeEventLoop):
  def initialise(self, commands, handlers, prefix):
    self.commands = commands
    self.handlers = handlers
    self.prefix = prefix
  def onEvent(self, event):
    if isinstance(event, SkypeNewMessageEvent) and event.msg.userId != self.userId:
      for handler in self.handlers:
        if handler[0]:
          Thread(target=handler[2], args=(event.msg,), daemon=handler[1]).start()
        else:
          handler[2](event.msg)
      for command in self.commands:
        if event.msg.content.startswith(self.prefix+command[0]):
          arguments = parse_args(event.msg.content.split(self.prefix+command[0])[1], command[2])
          Thread(target=command[1], args=(event.msg, arguments), daemon=True).start()

class Message:
  def __init__(self, prefix):
    if prefix == '/':
      raise ValueError('Prefix cannot be /.')
      sys.exit(1)
    self.commands = []
    self.handlers = []
    self.prefix = prefix
  def handler(self, thread:bool=True, daemon:bool=True):
    def inner(func):
      self.handlers.append((thread, daemon, func))
    return inner
  def command(self, name:str, arguments:list=[], thread:bool=True, daemon:bool=True):
    def inner(func):
      self.commands.append((name, func, arguments, thread, daemon))
    return inner

def login(commands, email, password):
  skype = SkypePing(user=email, pwd=password, autoAck=True)
  skype.initialise(commands.commands, commands.handlers, commands.prefix)
  skype.loop()
