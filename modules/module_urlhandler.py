# -*- coding: utf-8 -*-

# this module do url handling, by displaying url title into channel and
# adding it to the database.
# links are accesible via !link command, which accept argument for link search
# based on original pyfibot "module_urltitle"

import fnmatch
import logging
import re
import datetime
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

        # insert the link in the DB
        dbCursor.execute("SELECT link_id FROM links WHERE link_url = '%s'" % url)
        comp = dbCursor.fetchone()
        if not comp:
            bot.log("Added link to db: %s" % unicode(url, 'utf-8'))
            dbCursor.execute("INSERT INTO links VALUES (NULL,?,?,?,?)",
            (unicode(url,'utf-8'),unicode(str(title),'utf-8'), datetime.date.today(), getNick(user)))

    except AttributeError:
        # TODO: Nees a better way to handle this
        # this happens with empty <title> tags
        pass


def command_link(bot, user, channel, args):
    """show stored links, accept arguments"""

    if args:

        if "'" in args:
            return bot.say(channel, 'hax0r')

        dbCursor.execute("SELECT link_url, link_title FROM links WHERE link_title REGEXP '.*?%s.*?' ORDER BY RANDOM() LIMIT 1" % (unicode(args, 'utf-8')))
        comp = dbCursor.fetchone()
        if comp:
            bot.say(channel, '%s (%s)' % (comp[0].encode("utf-8"), comp[1].encode("utf-8")))

        else:
            bot.say(channel,'%s not found, %s' % (args, getNick(user)))

    else:
        dbCursor.execute("SELECT link_url, link_title FROM links ORDER BY RANDOM() LIMIT 1")
        comp = dbCursor.fetchone()
        bot.say(channel, '%s (%s)' % (str(comp[0].encode("utf-8")), comp[1].encode("utf-8")))
