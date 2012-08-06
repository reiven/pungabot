import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


def command_dolar(bot, user, channel, args):
    """show the dollar exchange in .ar"""

    page = urllib2.urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class": "cotizaciones3"})
    bot.say(channel, '%s compra - %s venta' % (
        tabla[0].renderContents().strip(),
        tabla[1].renderContents().strip()
        ))
    return


def command_euro(bot, user, channel, args):
    """show the euro exchange in .ar"""

    page = urllib2.urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class": "cotizaciones3"})
    bot.say(channel, '%s compra - %s venta' % (
        tabla[2].renderContents().strip(),
        tabla[3].renderContents().strip()
        ))
    return


def command_riesgopais(bot, user, channel, args):
    """show current argentina's country risk index"""

    page = urllib2.urlopen("http://www.riesgopais.com")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("table", {"width": "480"})
    datos = tabla[0].find('td', attrs={'valign': 'top'})
    final = unicode(datos.findAll(text=True)).split("\\")
    bot.say(channel, '%s' % final[4].split('n')[1].encode("utf-8"))
    return
