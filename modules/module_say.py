def privcommand_say(bot, user, channel, args):
    """pulic say to a channel Usage: say #channel (message) """

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:

        if len(args.split()) >= 2:
            where, tosay = args.split(None, 1)
            if where in bot.network.channels:
                bot.say(where, '%s' % tosay.strip())

            else:
                bot.say(user, "i dont know that channel")

        else:
            bot.say(user, "wrong usage, see help")
