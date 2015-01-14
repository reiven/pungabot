# -*- coding: utf-8 -*-

import feedparser
import unicodedata
import re
import string
import Stemmer

FEEDS = {
    'Clarín': 'http://www.clarin.com/rss/',
    'InfoBAE': 'http://www.infobae.com/rss',
    'La Nacion': 'http://contenidos.lanacion.com.ar/herramientas/rss/origen=2',
    'La Prensa': 'http://www.laprensa.com.ar/ResourcesManager.aspx?Resource=Rss.aspx&Rss=4',
    'Pagina12': 'http://www.pagina12.com.ar/diario/rss/principal.xml',
    'Perfil': 'http://www.perfil.com/rss/ultimomomento.xml',
    'BBC Mundo': 'http://www.bbc.co.uk/mundo/index.xml',
    'Agencia Noticias Bariloche': 'http://www.anbariloche.com.ar/rss',
    'El Cronista': 'http://www.cronista.com/rss.html',
}


def sanitize(buf):
    return filter(lambda x: x in string.printable, buf)


def noticias(busqueda):
    regexps = [re.compile(sanitize(busqueda), re.MULTILINE | re.IGNORECASE)]
    ret = []
    for feed_name, feed_source in FEEDS.iteritems():
        for entry in feedparser.parse(feed_source).entries:
            for r in regexps:
                if r.search(entry.title):
                    ret.append(feed_name + ': ' + unicodedata.normalize('NFKD', entry.title).encode('ascii', 'ignore') + ' (' + unicodedata.normalize('NFKD', entry.link).encode('ascii', 'ignore') + ')')

    return ret


def command_noticia(bot, user, channel, args):
    """search for keyword in FEEDS """

    if args:
        # replace the stemmer with your lang
        stemmer = Stemmer.Stemmer('spanish')
        feed_name = noticias(stemmer.stemWord(args))
        if len(feed_name) == 0:
            bot.say(channel, 'sorry, %s not found' % args)
            return

        else:
            for i in range(0, len(feed_name), 1):
                if i == 3:
                    return

                else:
                    bot.say(channel, '%s' % (feed_name[i]))

    else:
        return bot.say(channel, '%s: search for what?' % getNick(user))
