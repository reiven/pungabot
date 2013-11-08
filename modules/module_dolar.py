from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


def command_dolar(bot, user, channel, args):
    """show the dollar exchange in .ar"""

    page = urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class": "cotizaciones3"})
    bot.say(channel, '%s compra - %s venta' % (
        tabla[0].renderContents().strip(),
        tabla[1].renderContents().strip()
        ))
    return


def command_euro(bot, user, channel, args):
    """show the euro exchange in .ar"""

    page = urlopen("http://www.cotizacion-dolar.com.ar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tabla = soup.findAll("td", {"class": "cotizaciones3"})
    bot.say(channel, '%s compra - %s venta' % (
        tabla[2].renderContents().strip(),
        tabla[3].renderContents().strip()
        ))
    return


def command_riesgopais(bot, user, channel, args):
    """show current argentina's country risk index"""

    page = urlopen("http://www.ambito.com/economia/mercados/riesgo-pais/info/?id=2")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    valor = soup.findAll("div", {"id": "ultimo"})
    variacion = soup.findAll("div", {"id": "variacion"})
    bot.say(channel, '%s (%s)' % (
        valor[0].findAll("big")[0].renderContents(),
        variacion[0].findAll("big")[0].renderContents()
    ))
    return


def command_ccl(bot, user, channel, args):
    """show referencial value for 'contado con liquidacion'"""

    page = urlopen("http://www.ambito.com/economia/mercados/monedas/dolar/")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    div = soup.findAll("div", {"class": "bonosPrincipal dolarPrincipal"})
    valor = div[3].findAll("div", {"class": "cierreAnteriorUnico"})
    variacion = div[3].findAll("div", {"class": "variacion"})
    bot.say(channel, '$%s (%s)' % (
        valor[0].findAll("big")[0].renderContents(),
        variacion[0].findAll("big")[0].renderContents()
    ))
    return


def command_bitcoin(bot, user, channel, args):
    """show last bitcoin value, based on bitcoinity.org"""

    page = urlopen("http://bitcoinity.org/markets")
    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    div = soup.findAll("div", {"class": "last_prices"})
    valor = div[0].findAll("span", {"id": "last_price"})
    bot.say(channel, '$%s USD/BTC' % (
        valor[0].renderContents(),
    ))
    return
