import urllib2, re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import unicodedata

def command_dolar(bot,user, channel, args):
    """show the dollar exchange in .ar"""

    page = urllib2.urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class" : "cotizaciones3"})
    bot.say(channel,'%s compra - %s venta' % (tabla[0].renderContents().strip(),tabla[1].renderContents().strip()))
    return

def command_euro(bot,user, channel, args):
    """show the euro exchange in .ar"""

    page = urllib2.urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class" : "cotizaciones3"})
    bot.say(channel,'%s compra - %s venta' % (tabla[2].renderContents().strip(),tabla[3].renderContents().strip()))
    return
