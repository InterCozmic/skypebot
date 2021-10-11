import main
from skpy.msg import SkypeMsg

message = main.Message('!') #the message receiver. replace '!' with your bot's prefix (this could be anything, but don't make it '/', because Skype already has other '/' commands)

username = 'example@example.com' #this should be the email that the bot's Skype account is registered under
password = 'password123' #this should be the password for the bot's Skype account

@message.customhandler() #a custom handler - it's in the name
def receive(message): 
  message.chat.sendMsg(f'{SkypeMsg.bold("Message received!")} Content: {message.content}', rich=True)
  #Okay - here's a breakdown.
  #message.chat.sendMsg is a built-in method from SkPy, and it sends a message to the chat.
  #SkypeMsg.bold() is another SkPy method, and that formats the text as bold.
  #message.content is the message's content.
  #rich=True specifies that text formatting should be taken into account - this HAS to be used as a parameter if sending messages with bold, italics, strikethrough - any formatting, really.

@message.command('hi') #a command - activated with '!hi'
def function(message, args):
  #here, args does nothing since there are no arguments.
  message.chat.sendMsg('Hello') #sends 'hello' back

main.login(message, username, password) #log in