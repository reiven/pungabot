# -*- coding: utf-8 *-*
import requests
import json


def command_stock(bot, user, channel, args):
    """show current information about a financial symbol"""
    prefix = "http://finance.google.com/finance/info?client=ig&q="
    url = ''.join([prefix, args])
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.text[3:])[0]
        bot.say(channel, "(%s:%s) %s (%s %%)" % (
            data['e'].encode('utf-8'),
            data['t'].encode('utf-8'),
            data['l_fix'].encode('utf-8'),
            data['cp_fix'].encode('utf-8'))
            )
    else:
        bot.say(channel, "sorry, that is not a valid company symbol")
