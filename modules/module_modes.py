# -*- coding: utf-8 -*-

# this module handle all the commands related to mode / topic changes

import hashlib
from pysqlite2 import dbapi2 as sqlite3

##################################################################

def handle_modeChanged(bot, user, channel, set, modes, args):
    """Mode changed on user or channel"""

    bot.log("%s - %s - %s - %s - %s" % (getNick(user), channel, set, modes, args))
    bot.getNames(channel)
    return

##################################################################

def privcommand_topic(bot, user, channel, args):
    """Usage: !topic #channel (new topic message)"""

    if bot.checkValidHostmask(user):
	if args: 
	    if channel in bot.network.channels:
		bot.topic(channel,args)
		bot.say(user, 'ok, topic changed on %s' % channel)

    	    else:
		bot.say(channel, 'sorry, i dont know that channel ')

	else:
    	    bot.say(channel, "Usage error.  See 'help names'")


##################################################################

def privcommand_names(bot, user, channel, args):
    """Show users in #channel"""

    if bot.checkValidHostmask(user):
	if args: 
	    if args in bot.network.channels:
		users = bot.getNames(args)
		for u in users:
		    bot.say(channel,"%s" % (u))

    	    else:
		bot.say(channel, 'sorry, i dont know that channel ')

	else:
    	    bot.say(channel, "Usage error.  See 'help names'")

##################################################################

def privcommand_op(bot, user, channel, args):
    """!op (password) user channel - Mode +o the specified user"""

    if bot.checkValidHostmask(user):
        if len(args.split()) == 3:
            passwd,toop,w2o = args.split()
	    if w2o in bot.network.channels:
        	passwd = hashlib.sha1(passwd).hexdigest()
        	conn = sqlite3.connect(bot.nickname + ".db")
        	cursor = conn.cursor()
        	cursor.execute("SELECT name FROM users where passwd = '%s'" % passwd)
        	comp = cursor.fetchone()
        	if comp:
		    bot.log('%s requested op for %s on %s' % (str(comp[0]),toop,w2o))
    		    bot.mode(w2o, 1, 'o', user=toop)

    	    else:
		bot.say(channel, 'sorry, i dont know that channel ')

	else:
    	    bot.say(channel, "Usage error.  See 'help op'")

def privcommand_deop(bot, user, channel, args):
    """Usage: deop (password) user channel - Mode -o the specified user"""

    if bot.checkValidHostmask(user):
        if len(args.split()) == 3:
            passwd,deop,w2o = args.split()
	    if w2o in bot.network.channels:
        	passwd = hashlib.sha1(passwd).hexdigest()
        	conn = sqlite3.connect(bot.nickname + ".db")
        	cursor = conn.cursor()
        	cursor.execute("SELECT name FROM users where passwd = '%s'" % passwd)
        	comp = cursor.fetchone()
        	if comp:
		    bot.log('%s requested deop for %s on %s' % (str(comp[0]),deop,w2o))
    		    bot.mode(w2o, 0, 'o', user=deop)

    	    else:
		bot.say(channel, 'sorry, i dont know that channel ')

	else:
    	    bot.say(channel, "Usage error.  See 'help deop'")

