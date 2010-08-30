import string
from util import pyfiurl

""" this will only log public messages, which not include url or commands, and split
    the message if it quotes someone"""


def handle_privmsg (bot, user, channel, msg):

    if not channel.lower() == bot.nickname.lower() and not msg.startswith("!") and not pyfiurl.grab(msg):
	f = open("logger.txt","a")

	if ':' in msg:
	    msg = msg[(msg.find(':'))+1:]

	f.write(msg.strip()+"\n")
	bot.log("%s" % msg.strip())
	f.close()
