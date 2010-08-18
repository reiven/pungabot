
import urllib2, re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import unicodedata

def command_futbol(bot,user, channel, args): 
    """ show different argentine's footbal stats"""

    if args:
	if args.lower() == "posiciones":

	    page = urllib2.urlopen("http://www.bofh.net.ar/primera-division.html")
	    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

	    tabla = soup.findAll("div", {"id" : "tabla_posiciones"})
	    equipos = tabla[0].findAll('td',{'class' : 'ancho-160'})
	    puntos = tabla[0].findAll('p',{'class' : 'pts'})
	    for i in range (0,5):
		e = equipos[i].findAll('a')
		bot.say(channel,'%s - %s puntos' % (e[0].renderContents(),puntos[i].renderContents()))

	    return

	elif args.lower() == "goleadores":

	    page = urllib2.urlopen("http://www.bofh.net.ar/primera-division.html")
	    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

	    tabla = soup.findAll("div", {"id" : "tabla_goleadores"})
	    datos = tabla[0].findAll('td')

	    for i in range (0,45,9):
		e = datos[i+3].findAll('a')
		bot.say(channel,'%s - %s - %s goles' % (datos[i+1].renderContents(),e[0].renderContents(), datos[i+8].find('p').renderContents()))

	    return

	elif args.lower() == "promedio":

	    page = urllib2.urlopen("http://www.bofh.net.ar/primera-division.html")
	    soup = BeautifulSoup(page, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

	    tabla = soup.findAll("div", {"id" : "tabla_descenso"})
	    datos = tabla[0].findAll('td')

	    for i in range (152,112,-8):
		e = datos[i+1].findAll('a')
		bot.say(channel,'%s - %s' % (e[0].renderContents(),datos[i+7].renderContents()))

	    return

        else:
	    return bot.say(channel,'subcommands: posiciones / goleadores / promedio')

    else:
	return bot.say(channel,'subcommabds: posiciones / goleadores / promedio')