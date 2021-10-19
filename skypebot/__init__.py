from skpy import SkypeEventLoop, SkypeNewMessageEvent
from threading import Thread
import re
from bs4 import BeautifulSoup

class ParsedArgumentsObject:
  def __init__(self, users: list, **kwargs):
    self.users: list["ParsedUser"] = users
    for key, value in kwargs.items():
      setattr(self, key, value)

class ParsedUser:
  def __init__(self, id, name):
    self.id: str = id
    self.name: str = name

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

class _SkypePing(SkypeEventLoop):
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
    self.commands = []
    self.handlers = []
    self.prefix = prefix
  def handler(self, thread:bool=True, daemon:bool=True):
    def inner(func):
      self.handlers.append((thread, daemon, func))
    return inner
  def command(self, name:str, arguments:list[str]=[], thread:bool=True, daemon:bool=True):
    def inner(func):
      self.commands.append((name, func, arguments, thread, daemon))
    return inner

def login(commands, email, password):
  skype = _SkypePing(user=email, pwd=password, autoAck=True)
  skype.initialise(commands.commands, commands.handlers, commands.prefix)
  skype.loop()

if __name__ == "__main__":
  #Example Code
  #If you use this in your bot, make sure to un-comment the following line to import the module:
  #from skypebot import *

  email = input('Email: ')
  password = input('Password: ')
  message = Message('!') #initialise message with the prefix '!'

  #example of a message handler
  @message.handler() #custom handler
  def messagehandle(message):
    print(str(message.user.name)+': '+message.content) #print the message's author and content

  #example of a basic command
  @message.command('hi') #hi command - can be accessed in Skype by typing '!hi'
  def hi(message, arguments):
    message.chat.sendMsg('hello') #send 'hello' back.

  #example of a command with arguments
  @message.command('repeat', ['times', 'thing']) #repeat command - can be accessed in Skype by typing '!repeat <number_of_times> <thing_to_repeat>'
  def repeater(message, arguments):
    string = arguments.thing + '\n' #create a string with the thing to repeat
    string = string * int(arguments.times) #repeat that thing multiple times
    message.chat.sendMsg(string) #send to chat

  login(message, email, password) #log in to the bot
