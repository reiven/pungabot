# -*- coding: utf-8 -*-

##################################################################

def handle_modeChanged(bot, user, channel, set, modes, args):
    """Mode changed on user or channel"""

    bot.log("%s - %s - %s - %s - %s" % (getNick(user), channel, set, modes, args))
    bot.getNames(channel)
    return

##################################################################

def handle_topicUpdated(bot, user, channel, newtopic):

    bot.log ('%s chaged topic to %s on %s' % (getNick(user),newtopic,channel))

##################################################################

def privcommand_topic(bot, user, channel, args):
    """Usage: !topic #channel (new topic message)"""

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

def privcommand_isopped (bot, user, channel, args):

    opped = '@' + getNick(user)

    if opped in users:
	bot.say(channel,"you are opped %s" % getNick(user))
    else:
	bot.say(channel,"not opped")

##################################################################

def privcommand_op(bot, user, channel, args):
    """!op (password) user channel - Mode +o the specified user"""

    if len(args.split()) == 3:
	password, toop , w2o = args.split()
	if password == "password":
	    if w2o in bot.network.channels:

		bot.say(channel, '%s requested op for %s on %s' % (getNick(user),toop,w2o))
    		bot.mode(w2o, 1, 'o', user=toop)

    	    else:
		bot.say(channel, 'sorry, i dont know that channel ')

    else:
        bot.say(channel, "Usage error.  See 'help op'")


def privcommand_deop(bot, user, channel, args):
    """Usage: deop (password) username - Mode -o the specified user"""

    if len(args.split()) == 3:
	password, deop , w2d= args.split()
	if password == "password":
	    if w2d in bot.network.channels:
		bot.say(channel, '%s requested deop for %s on %s' % (getNick(user),deop,w2d))
    		bot.mode(w2d, 0, 'o', user=deop)

    	    else:
		bot.say(channel, 'sorry, i dont know that chanel ')

    else:
        bot.say(channel, "Usage error.  See 'help op'")

