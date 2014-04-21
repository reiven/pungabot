# -*- coding: utf-8 -*-
import string
import Stemmer


def sanitize(buf):
    return filter(lambda x: x in string.printable, buf)


def showQuote(bot, channel, comp):
    for line in str(comp[1]).split('|'):
       bot.say(channel, '%s' % line.encode("utf-8").strip())
    bot.say(channel, '(%s)' % str(comp[0]))
    return


def command_quote(bot, user, channel, args):
    """show quote. it accept arguments"""

    if args:

        if "'" in args:
            return bot.say(channel, 'hax0r')

        dbCursor.execute("SELECT quote_id, quote_text FROM quotes WHERE quote_channel = '%s' AND  quote_text REGEXP '.*?%s.*?' ORDER BY RANDOM() LIMIT 1" % (channel, unicode(args, 'utf-8')))
        comp = dbCursor.fetchone()
        if comp:
            showQuote(bot, channel, comp)
        else:
            bot.say(channel,'%s not found, %s' % (args, getNick(user)))

    else:
        dbCursor.execute("SELECT quote_id, quote_text FROM quotes WHERE quote_channel = '%s' ORDER BY RANDOM() LIMIT 1" % (channel))
        comp = dbCursor.fetchone()
        showQuote(bot, channel, comp)


def command_quotes(bot, user, channel, args):
    """show stemmer quote text"""

    if args:

        if "'" in args:
            return bot.say(channel, 'hax0r')

        # set stemmer lang to spanish
        stemmer = Stemmer.Stemmer('spanish')
        dbCursor.execute("SELECT quote_id, quote_text FROM quotes WHERE quote_channel = '%s' AND quote_text REGEXP '.*?%s.*?' ORDER BY RANDOM() LIMIT 1" % (channel, unicode(stemmer.stemWord(args), 'utf-8')))
        comp = dbCursor.fetchone()
        if comp:
            showQuote(bot, channel, comp)
        else:
            bot.say(channel,'%s not found, %s' % (args, getNick(user)))

    else:
        return bot.say(channel, '%s: what to do wanna search for?' % getNick(user))


def command_add(bot, user, channel, args):
    """add new quote"""

    if args:
        dbCursor.execute("INSERT INTO quotes VALUES (NULL, ?, '0', ?, ?)", (unicode(args, 'utf-8'), getNick(user), channel))

        if channel == "#pvm":
            for line in args.split('|'):
                if len(line) < 139:
                    twapi.update_status(unicode(line.strip(),'utf-8'))
                else:
                    bot.say(channel, '%s,uhm i failed to update twitter in some way' % getNick(user))

        bot.say(channel, 'ok,%s quote added' % getNick(user))
        # check quote number
        dbCursor.execute("SELECT quote_id FROM quotes ORDER BY quote_id DESC LIMIT 1")
        comp = dbCursor.fetchone()
        if (int(comp[0]) % 100 == 0):
            bot.say(channel, 'wohooooo! %s quotes!!!! a chriunfaaaa!!!' % int(comp[0]))

    else:
        bot.say(channel, '%s: what do you want to add?' % getNick(user))


def command_lastquote(bot, user, channel, args):
    """show last added quote"""

    dbCursor.execute("SELECT quote_id, quote_text FROM quotes WHERE quote_channel = '%s' ORDER BY quote_id DESC LIMIT 1" % (channel))
    comp = dbCursor.fetchone()

    showQuote(bot, channel, comp)


def command_show(bot, user, channel, args):
    """show especific quote by id"""

    if args:
        if "'" in args:
            return bot.say(channel, 'hax0r')

        dbCursor.execute("SELECT quote_id, quote_text, quote_channel FROM quotes WHERE quote_id = '%s' LIMIT 1" % sanitize(args))
        comp = dbCursor.fetchone()
        if comp:
            if str(comp[2]) == channel:
                showQuote(bot, channel, comp)
            else:
                bot.say(channel, '%s: sorry but that quote is from another channel' % (getNick(user)))
        else:
            bot.say(channel, '%s: %s is cualquiera, not found' % (getNick(user),args))
    else:
        bot.say(channel, '%s: what id do you wanna see?' % getNick(user))

