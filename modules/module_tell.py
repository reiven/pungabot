# -*- coding: utf-8 -*-
import string
from datetime import datetime


def sanitize(buf):
    return filter(lambda x: x in string.printable, buf)


def handle_userJoined(bot, user, channel):
    """Someone Joined, lets salute him"""

    dbCursor.execute("SELECT * FROM tell WHERE tell_to = '%s' AND tell_channel = '%s'" % (getNick(user), channel ))
    rows = dbCursor.fetchall()
    for row in rows:
        bot.say(channel, '%s: %s leaved this message for you on %s at %s:' % (
            getNick(user),
            row[1].encode("utf-8"),
            row[3].split()[0],
            row[3].split()[1],
            ))
        bot.say(channel, '"%s"' % row[4].encode("utf-8"))
        dbCursor.execute("DELETE FROM tell WHERE tell_id = '%s'" % row[0])


def command_tell(bot, user, channel, args):
    """tell something to user when he/she rejoin the channel"""

    if len(args.split()) >= 2:
        tell_to, args = args.split(' ', 1)
        dbCursor.execute("INSERT INTO tell VALUES (NULL, ?, ?, ?, ?, ?)", (
            getNick(user),
            unicode(tell_to, 'utf-8'),
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            unicode(args, 'utf-8'),
            channel
            ))
        return bot.say(channel, '%s, i will tell that to %s'  % (getNick(user), unicode(tell_to, 'utf-8') ))

    else:
        return bot.say(channel, '%s, for who and what you save a message?' % getNick(user))
