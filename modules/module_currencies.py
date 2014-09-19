# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import requests


def percent_variation(new, old):
    return ((float(new) / float(old)) * 100) - 100


def command_dolar(bot, user, channel, args):
    """show the dollar exchange in .ar"""

    r = requests.get('http://www.cotizacion-dolar.com.ar/')
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.text,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        tabla = soup.findAll("td", {"class": "cotizaciones3"})
        return bot.say(channel, '%s compra - %s venta (ARS/USD)' % (
            tabla[0].renderContents().strip(),
            tabla[1].renderContents().strip()
            ))
    else:
        return bot.say(channel, 'sorry, something wrong with server')


def command_euro(bot, user, channel, args):
    """show the euro exchange in .ar"""

    r = requests.get('http://www.cotizacion-dolar.com.ar/')
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.text,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        tabla = soup.findAll("td", {"class": "cotizaciones3"})
        bot.say(channel, '%s compra - %s venta (ARS/€)' % (
            tabla[2].renderContents().strip(),
            tabla[3].renderContents().strip()
            ))
    else:
        return bot.say(channel, 'sorry, something wrong with server')


def command_riesgopais(bot, user, channel, args):
    """show current argentina's country risk index"""

    r = requests.get(
        'http://www.ambito.com/economia/mercados/riesgo-pais/info/?id=2'
        )
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.text,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        valor = soup.findAll("div", {"id": "ultimo"})
        variacion = soup.findAll("div", {"id": "variacion"})
        return bot.say(channel, '%s (%s)' % (
            valor[0].findAll("big")[0].renderContents(),
            variacion[0].findAll("big")[0].renderContents()
        ))
    else:
        return bot.say(channel, 'sorry, something wrong with server')


def command_ccl(bot, user, channel, args):
    """show referencial value for 'contado con liquidacion'"""

    r = requests.get('http://www.ambito.com/economia/mercados/monedas/dolar/')
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.text,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        div = soup.findAll("div", {"class": "bonosPrincipal dolarPrincipal"})
        valor = div[4].findAll("div", {"class": "cierreAnteriorUnico"})
        variacion = div[4].findAll("div", {"class": "variacion"})
        return bot.say(channel, '$%s (%s)' % (
            valor[0].findAll("big")[0].renderContents(),
            variacion[0].findAll("big")[0].renderContents()
        ))
    else:
        return bot.say(channel, 'sorry, something wrong with server')


def command_blue(bot, user, channel, args):
    """show referencial value for black market dollar in .ar"""

    r = requests.get('http://www.ambito.com/economia/mercados/monedas/dolar/')
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.text,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
            )
        div = soup.findAll("div", {"class": "bonosPrincipal dolarPrincipal"})
        compra = div[2].findAll("div", {"class": "ultimo"})
        venta = div[2].findAll("div", {"class": "cierreAnterior"})
        variacion = div[2].findAll("div", {"class": "variacion"})
        return bot.say(channel, '%s compra - %s venta (%s) (ARS/USD)' % (
            compra[0].findAll("big")[0].renderContents(),
            venta[0].findAll("big")[0].renderContents(),
            variacion[0].findAll("big")[0].renderContents()
        ))
    else:
        return bot.say(channel, 'sorry, something wrong with server')


def command_bitcoin(bot, user, channel, args):
    """show bitcoin exchange value, based on blockchain.info API"""

    r = requests.get('https://blockchain.info/es/ticker')
    if r.status_code == 200:
        data = r.json()
        return bot.say(channel, '%s compra - %s venta (USD/XBT)' % (
            data['USD']['buy'],
            data['USD']['sell'],
        ))
    else:
        return bot.say(channel, 'cannot get data from cryptocoincharts API')


def command_litecoin(bot, user, channel, args):
    """show litecoin exchange value, based on cryptocoincharts.info API"""

    r = requests.get(
        'http://api.cryptocoincharts.info/tradingPair/ltc_usd'
        )
    if r.status_code == 200:
        data = r.json()
        return bot.say(channel, '%s (%2.3f %%) (USD/LTC)' % (
            data['price'].encode('utf-8'),
            percent_variation(data['price'], data['price_before_24h'])
            ))
    else:
        return bot.say(channel, 'cannot get data from cryptocoincharts API')


def command_dogecoin(bot, user, channel, args):
    """show dogecoin exchange value, based on cryptocoincharts.info API"""

    r = requests.get(
        'http://api.cryptocoincharts.info/tradingPair/doge_usd'
        )
    if r.status_code == 200:
        data = r.json()
        return bot.say(channel, '%s (%2.3f %%) (USD/XDG)' % (
            data['price'].encode('utf-8'),
            percent_variation(data['price'], data['price_before_24h'])
            ))
    else:
        return bot.say(channel, 'cannot get data from cryptocoincharts API')


def command_darkcoin(bot, user, channel, args):
    """show dogecoin exchange value, based on cryptocoincharts.info API"""

    r = requests.get(
        'http://api.cryptocoincharts.info/tradingPair/drk_usd'
        )
    if r.status_code == 200:
        data = r.json()
        return bot.say(channel, '%s (%2.3f %%) (USD/DRK)' % (
            data['price'].encode('utf-8'),
            percent_variation(data['price'], data['price_before_24h'])
            ))
    else:
        return bot.say(channel, 'cannot get data from cryptocoincharts API')
