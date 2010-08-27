# -*- coding: utf-8 -*-

import re

def handle_privmsg (bot, user, channel, message):

    MSG = ['papel' ,'merca' ,'blanca', 'cameruza', 'tripa','pepa','trip',
	    'porro','faso','churro','maconia','fumar','volar']
    regex = re.compile('(' + '|'.join(MSG) + ')', re.IGNORECASE)

    if regex.findall(message):
	for loque in regex.findall(message):
	    bot.say(channel, "dijo %s!! JA"  % loque)

