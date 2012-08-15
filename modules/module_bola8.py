import random


def command_bola8(bot, user, channel, args):
    """show eight-ball answer"""

    if args:
        bot.log("bola8 called on %s" % channel)
        eightball = ['como patada ninja', 'seh, a pleno', 'sin duda',
            'tal como lo veo, si', 'apa! sisi', 'seguro!', 'decididamente si',
            '..bastante', 'claro', 'y.. apunta a que si', 'sin duda', 'sale',
            'sisisi,si!', 'si, definitivamente',
            'tan cierto como la ley de la gravedad', 'lo que?', 'wtf??',
            'no entiendo', 'la verdad q ni idea', 'nusep',
            'estas seguro que queres saber?', 'no podria afirmarlo',
            'ignorance is bliss', 'no estoy seguro',
            'uhm es medio rantesco, no se', 'ni siquiera lo pienses',
            'mi respuesta es NO', 'nah, ni ahi', 'ni en pedo',
            'uhmmmmmmmmmmm', 'el dia que los natas vuelen..',
            'estas hablando del fffffassssoooooooo?']
        return bot.say(channel, '%s' % random.choice(eightball))

    else:
        return bot.say(channel, 'que queres preguntar, %s?' % getNick(user))


def handle_privmsg(bot, user, channel, msg):

    if not channel.lower() == bot.nickname.lower():

        # public direct message to the bot
        if msg.startswith(bot.nickname):
            command_bola8(bot, user, channel, msg)
