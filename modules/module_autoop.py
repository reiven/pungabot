

def handle_userJoined(bot, user, channel):
    """ only auto-op bot and masters"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 4:
        bot.log("auto-opping %s" % user)
        bot.mode(channel, True, 'o', user=getNick(user))
