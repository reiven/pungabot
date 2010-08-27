# -*- coding: utf-8 -*-

import re
import random

def handle_privmsg (bot, user, channel, message):

    ono = random.randrange(10)
    # we have a chances of 30% of use this module
    if ono < 7:
        return

    MSG = ['papel' ,'merca' ,'blanca', 'cameruza', 'pala','pase','toque',
            'pasta','bicho',
            'tripa','pepa','trip','carton','gotero','gota',
            'porro','faso','churro','maconia','fumar','volar']
    regex = re.compile('(' + '|'.join(MSG) + ')', re.IGNORECASE)

    if regex.findall(message):
	for loque in regex.findall(message):
	    bot.say(channel, "dijo %s!! JA"  % loque)

