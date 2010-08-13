from util import pyfiurl

def privcommand_twupdate(bot,user,channel,args):
    """update pycookibot status on twitter"""
    if isAdmin(user):
        if args:
	    twupdate(args)
    	    return bot.say(channel, '%s, status updated' % getNick(user))

	else:
	    return bot.say(channel,'%s, what do you wanna post to tw?' % getNick(user))

    return bot.say(channel,'%s, you are not admin.. sry' % getNick(user))

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
	    bot.say(channel, '%s: no parece que %s sea un twitter valido' % (getNick(user), args))

    else:
	return bot.say(channel, '%s, mostrar el status de quien?' % getNick(user))