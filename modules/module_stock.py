# -*- coding: utf-8 *-*
import urllib2
import xml.etree.ElementTree as xml

""" google finance api url """
GOOGLE_STOCK_URL = 'http://www.google.com/ig/api?stock=%s'


def command_stock(bot, user, channel, args):
    """show current information about a financial symbol"""

    tree = xml.parse(urllib2.urlopen(GOOGLE_STOCK_URL % args))
    doc = tree.getroot()
    finance = doc.find('finance')
    if finance.find('exchange').attrib.values()[0] != "UNKNOWN EXCHANGE":
        bot.say(channel, "(%s:%s) %s : %s %s (%s %%)" %
            (finance.find('exchange').attrib.values()[0],
            finance.find('symbol').attrib.values()[0],
            finance.find('company').attrib.values()[0],
            finance.find('currency').attrib.values()[0],
            finance.find('last').attrib.values()[0],
            finance.find('perc_change').attrib.values()[0]))

    else:
        bot.say(channel, "sorry, that is not a valid company symbol")
