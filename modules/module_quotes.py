# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite3
import re
import string
import os
import Stemmer

def sanitize(buf):
    return filter(lambda x: x in string.printable,buf)

def regexp(expr, item): 
    r = re.compile(expr, re.MULTILINE | re.IGNORECASE)
    return r.match(item) is not None

def getConn(db):
    conn = sqlite3.connect(db)
    conn.create_function("regexp", 2, regexp)
    return conn.cursor()

def getQuote(cursor,channel,quoteId):
    cursor.execute("SELECT quote_id, quote_text FROM quotes WHERE quote_id = '%s' LIMIT 1" % quoteId)
    comp = cursor.fetchone()
    return (comp[1].encode("utf-8") + '| (' + str(comp[0]) + ')')

def command_quote(bot,user, channel, args):
    """show quote. it accept arguments"""

    if args:

	if "'" in args: 
	    return bot.say(channel,'hax0r')

	cursor = getConn(str.join('.',(bot.nickname , 'db')))
	cursor.execute("SELECT quote_id FROM quotes WHERE quote_text REGEXP '.*?%s.*?' ORDER BY RANDOM() LIMIT 1" % (unicode(args,'utf-8')))
	comp = cursor.fetchone()
	if comp:
	    quoteId = str(comp[0])
	    for line in getQuote(cursor,channel,quoteId).split('|'):
		bot.say(channel,'%s' % line.strip())

	else:
	    bot.say(channel,'%s not found, %s' % (args, getNick(user)))

    else:
	cursor = getConn(str.join('.',(bot.nickname , 'db')))
	cursor.execute("SELECT quote_id FROM quotes ORDER BY RANDOM() LIMIT 1")
	comp = cursor.fetchone()
	quoteId = str(comp[0])
    	for line in getQuote(cursor,channel,quoteId).split('|'):
	    bot.say(channel,'%s' % line.strip())

    conn.close()

def command_quotes(bot,user, channel, args):
    """show stemmer quote text"""

    if args:

	if "'" in args: 
	    return bot.say(channel,'hax0r')

	stemmer = Stemmer.Stemmer('spanish')
	cursor = getConn(str.join('.',(bot.nickname , 'db')))
	cursor.execute("SELECT quote_id FROM quotes WHERE quote_text REGEXP '.*?%s.*?' ORDER BY RANDOM() LIMIT 1" % (unicode(stemmer.stemWord(args),'utf-8')))
	comp = cursor.fetchone()
	if comp:
	    quoteId = str(comp[0])
	    for line in getQuote(cursor,channel,quoteId).split('|'):
		bot.say(channel,'%s' % line.strip())

	else:
	    bot.say(channel,'%s not found, %s' % (args, getNick(user)))

        conn.close()

    else:
	return bot.say(channel, '%s: what to do wanna search for?' % getNick(user))

def command_add(bot,user, channel, args):
    """add new quote"""

    if args:
	cursor = getConn(str.join('.',(bot.nickname , 'db')))
	cursor.execute("INSERT INTO quotes VALUES (NULL,?,'0',?)",(unicode(args,'utf-8'),getNick(user)))
        for line in args.split('|'):
                    twupdate(unicode(line.strip(),'utf-8'))

	conn.commit()
        bot.say(channel, 'ok,%s quote added' % getNick(user))
        # check quote number
        cursor.execute("SELECT quote_id FROM quotes ORDER BY quote_id DESC LIMIT 1")
        comp = cursor.fetchone()
        quoteId = int(comp[0])
        if (quoteId%100==0):
	    bot.say(channel, 'wohooooo! %s quotes!!!! a chriunfaaaa!!!' % quoteId)

	conn.close()

    else:
	bot.say(channel, '%s: what do you want to add?' % getNick(user))

def command_lastquote(bot,user, channel, args):
    """show last added quote"""

    cursor = getConn(str.join('.',(bot.nickname , 'db')))
    cursor.execute("SELECT quote_id FROM quotes ORDER BY quote_id DESC LIMIT 1")
    comp = cursor.fetchone()
    quoteId = str(comp[0])
    for line in getQuote(cursor,channel,quoteId).split('|'):
	bot.say(channel,'%s' % line.strip())

    conn.close()

def command_show(bot,user,channel,args):
    """show especific quote by id"""

    if args:
        if "'" in args:
            return bot.say(channel,'hax0r')

	cursor = getConn(str.join('.',(bot.nickname , 'db')))
	cursor.execute("SELECT quote_id FROM quotes WHERE quote_id = '%s' LIMIT 1" % sanitize(args))
	comp = cursor.fetchone()
	if comp:
	    quoteId = str(comp[0])
	    for line in getQuote(cursor,channel,quoteId).split('|'):
		bot.say(channel,'%s' % line.strip())

	else:
	    bot.say(channel,'%s: %s is cualquiera, not found' % (getNick(user),args))

	conn.close()

    else:
	bot.say(channel, '%s: what id do you wanna see?' % getNick(user))

