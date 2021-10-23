from . import Message, login

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