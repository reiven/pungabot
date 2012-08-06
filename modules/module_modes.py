# -*- coding: utf-8 -*-

# this module handle all the commands related to mode / topic changes

import hashlib


def handle_modeChanged(bot, user, channel, set, modes, args):
    """Mode changed on user or channel"""

    bot.log("%s - %s - %s - %s - %s" % (getNick(user), channel, set, modes, args))
    return


def privcommand_topic(bot, user, channel, args):
    """Usage: !topic #channel (new topic message)"""

    if bot.checkValidHostmask(user):
        bot.log("topic args: %s " % args)
        if len(args.split()) >= 2:
            w2ct, newtopic = args.split(' ',1)
            if w2ct in bot.network.channels:
                bot.log("ok, should change topic on %s" % w2ct)
                bot.topic(w2ct, newtopic)
                bot.say(channel, 'ok, topic changed on %s' % w2ct)

            else:
                bot.say(channel, 'sorry, i dont know that channel ')

        else:
            bot.say(channel, "Usage error.  See 'help topic'")


def privcommand_op(bot, user, channel, args):
    """!op (password) user channel - Mode +o the specified user"""

    if bot.checkValidHostmask(user):
        if len(args.split()) == 3:
            passwd, toop, w2o = args.split()
            if w2o in bot.network.channels:
                passwd = hashlib.sha1(passwd).hexdigest()
                dbCursor.execute("SELECT name FROM users where passwd = '%s'" % passwd)
                comp = dbCursor.fetchone()
                if comp:
                        bot.log('%s requested op for %s on %s' % (str(comp[0]), toop, w2o))
                        bot.mode(w2o, 1, 'o', user=toop)

            else:
                bot.say(channel, 'sorry, i dont know that channel ')

        else:
            bot.say(channel, "Usage error.  See 'help op'")


def privcommand_deop(bot, user, channel, args):
    """Usage: deop (password) user channel - Mode -o the specified user"""

    if bot.checkValidHostmask(user):
        if len(args.split()) == 3:
            passwd, deop, w2o = args.split()
            if w2o in bot.network.channels:
                passwd = hashlib.sha1(passwd).hexdigest()
                dbCursor.execute("SELECT name FROM users where passwd = '%s'" % passwd)
                comp = dbCursor.fetchone()
                if comp:
                    bot.log('%s requested deop for %s on %s' % (str(comp[0]), deop, w2o))
                    bot.mode(w2o, 0, 'o', user=deop)

            else:
                bot.say(channel, 'sorry, i dont know that channel ')

        else:
            bot.say(channel, "Usage error.  See 'help deop'")
