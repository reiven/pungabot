# -*- coding: utf-8 -*-

#
# we can use any method inside tweepy from modules, thanks to twapi global
#

from util import pyfiurl

def command_twitter(bot,user,channel,args):
    """ show last update from given twitter user"""

    if args:
	try:
	    status = twapi.user_timeline(args,count='1')

	except: 
	    return bot.say(channel, '%s: %s is not a valid twitter user' % (getNick(user), args))

	for s in status:
	    bot.say(channel, '%s: %s' % (args,s.text.encode('utf-8')))
	    urls = pyfiurl.grab(s.text.encode('utf-8'))
	    if urls:
    		for url in urls:
		    bot._runhandler("url", user, channel, url, args)

        return 

    else:
	return bot.say(channel, '%s, which user status you wanna see?' % getNick(user))

def privcommand_twupdate(bot,user,channel,args):
    """update bot status on twitter"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
        if args:
	    twapi.update_status( '%s' % args )
    	    return bot.say(user, 'ok %s, status updated' % getNick(user))

	else:
	    return bot.say(user,'%s, what do you wanna post to tw?' % getNick(user))

