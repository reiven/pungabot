# -*- coding: utf-8 *-*
import urllib2
import json


class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="

    def get(self, symbol):
        url = self.prefix + "%s" % (symbol)
        u = urllib2.urlopen(url)
        content = u.read()
        obj = json.loads(content[3:])
        return obj[0]


def command_stock(bot, user, channel, args):
    """show current information about a financial symbol"""
    c = GoogleFinanceAPI()
    quote = c.get(args)
    if quote['e'] != "UNKNOWN EXCHANGE":
        bot.say(channel, "(%s:%s) %s (%s %%)" % (
            quote['e'].encode('utf-8'),
            quote['t'].encode('utf-8'),
            quote['l_fix'].encode('utf-8'),
            quote['cp_fix'].encode('utf-8'))
            )

    else:
        bot.say(channel, "sorry, that is not a valid company symbol")
