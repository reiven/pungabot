# -*- coding: utf-8 -*-
"""Displays HTML page titles

Smart title functionality for sites which could have clear titles,
but still decide show idiotic bulk data in the HTML title element"""

import fnmatch
import logging
import re
from BeautifulSoup import BeautifulStoneSoup
log = logging.getLogger("urltitle")


def init(botconfig):
    global config
    config = botconfig.get("module_urltitle", {})


def handle_url(bot, user, channel, url, msg):
    """Handle urls"""

    if msg.startswith("-"):
        return

    if channel.lstrip("#") in config.get('disable', ''): return

    for ignore in config.get("ignore", []):
        if fnmatch.fnmatch(url, ignore):
            log.info("Ignored URL: %s %s", url, ignore)
            return


    bs = getUrl(url).getBS()
    if not bs:
        return

    title = bs.first('title')
    # no title attribute
    if not title:
        return

    try:
        # remove trailing spaces, newlines, linefeeds and tabs
        title = title.string.strip()
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        title = title.replace("\t", " ")

        # compress multiple spaces into one
        title = re.sub("[ ]{2,}", " ", title)

        # nothing left in title (only spaces, newlines and linefeeds)
        if not title:
            return

        if len(title) > 200:
            title = title[:200] + "..."

        title = BeautifulStoneSoup(
            title,
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES
            )

        bot.say(channel, "Title: '%s'" % title)

    except AttributeError:
        # TODO: Nees a better way to handle this
        # this happens with empty <title> tags
        pass
