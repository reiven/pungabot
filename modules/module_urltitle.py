# -*- coding: utf-8 -*-
"""Displays HTML page titles

Smart title functionality for sites which could have clear titles,
but still decide show idiotic bulk data in the HTML title element"""

import fnmatch
import htmlentitydefs
import urlparse
import logging
import re

from types import TupleType

from BeautifulSoup import BeautifulStoneSoup

log = logging.getLogger("urltitle")

def init(botconfig):
    global config
    config = botconfig.get("module_urltitle", {})

def handle_url(bot, user, channel, url, msg):
    """Handle urls"""

    if msg.startswith("-"): return
    if re.match("http://.*?\.imdb\.com/title/tt([0-9]+)/?", url): return # IMDB urls are handled elsewhere
    if re.match("(http:\/\/open.spotify.com\/|spotify:)(album|artist|track)([:\/])([a-zA-Z0-9]+)\/?", url): return # spotify handled elsewhere

    if channel.lstrip("#") in config.get('disable', ''): return

    for ignore in config.get("ignore", []):
        if fnmatch.fnmatch(url, ignore): 
            log.info("Ignored URL: %s %s", url, ignore)
            return


    bs = getUrl(url).getBS()
    if not bs: return

    title = bs.first('title')
    # no title attribute
    if not title: return

    try:
        # remove trailing spaces, newlines, linefeeds and tabs
        title = title.string.strip()
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        title = title.replace("\t", " ")

        # compress multiple spaces into one
        title = re.sub("[ ]{2,}", " ", title)

        # nothing left in title (only spaces, newlines and linefeeds)
        if not title: return

        if _check_redundant(url, title):
            return _title(bot, channel, title, redundant=True)   
        else:
            return _title(bot, channel, title)
    except AttributeError:
        # TODO: Nees a better way to handle this
        # this happens with empty <title> tags
        pass

def _check_redundant(url, title):
    """Returns true if the url already contains everything in the title"""
    
    buf = []
    for ch in url:
        if ch.isalnum(): buf.append(ch)
        url = (''.join(buf)).lower()
    buf = []
    for ch in title:
        if ch.isalnum() or ch == ' ': buf.append(ch)
        title = (''.join(buf)).lower().split()
    for word in title:
        if word not in url: return False

    return True

def _title(bot, channel, title, smart=False, redundant=False):
    """Say title to channel"""

    prefix = "Title:"

    if False:
        suffix = " [Redundant]"
    else:
        suffix = ""

    info = None
    # tuple, additional info
    if type(title) == TupleType:
        info = title[1]
        title = title[0]
    
    # crop obscenely long titles
    if len(title) > 200:
        title = title[:200]+"..."

    title = BeautifulStoneSoup(title, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    log.info(title)

    if not info:
        return bot.say(channel, "%s '%s'%s" % (prefix, title.encode('utf-8'), suffix))
    else:
        return bot.say(channel, "%s '%s' %s" % (prefix, title.encode('utf-8'), info))

