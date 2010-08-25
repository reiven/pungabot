# -*- coding: utf-8 -*-

from util import pyfiurl

def command_twitter(bot,user,channel,args):
    """ show last update from given twitter user"""

    if args:
	try:
	    status = twget (args)
	    bot.say(channel, '%s: %s' % (args,status))
	    urls = pyfiurl.grab(status)
	    if urls:
        	for url in urls:
            	    bot._runhandler("url", user, channel, url, args)

	    return 

	except: 
	    bot.say(channel, '%s: uhmf  %s is not a valid twitter user' % (getNick(user), args))

    else:
	return bot.say(channel, '%s, which user status you wanna see?' % getNick(user))

def privcommand_twupdate(bot,user,channel,args):
    """update bot status on twitter"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
        if args:
	    twupdate(args)
    	    return bot.say(channel, '%s, status updated' % getNick(user))

	else:
	    return bot.say(channel,'%s, what do you wanna post to tw?' % getNick(user))

