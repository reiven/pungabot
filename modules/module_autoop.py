def handle_userJoined(bot, user, channel):
    if isAdmin(user):
        bot.log("auto-opping %s" % user)
        bot.mode(channel, True, 'o', user=getNick(user))
