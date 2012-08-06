# -*- coding: utf-8 -*-

import re
import random


def handle_privmsg(bot, user, channel, message):

    # we have a chances of 30% of use this module
    if random.randrange(10) < 7:
        return

    MSG = ['papel', 'merca', 'blanca', 'cameruza', 'pala', 'pase', 'toque',
            'bolsa', 'pasta', 'bicho', 'pasteleta', 'pastilla', 'fafafa',
            'sarlanga', 'tripa', 'pepa', 'trip', 'carton', 'gotero', 'gota',
            'porro', 'faso', 'churro', 'maconia', 'fumar', 'yerba', 'volar']
    regex = re.compile('(' + '|'.join(MSG) + ')', re.IGNORECASE)

    if not message.startswith("!") and regex.findall(message):
        for loque in regex.findall(message):
            bot.say(channel, "dijo %s!! JA" % loque)
