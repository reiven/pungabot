# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite3
import hashlib
import string

def privcommand_auth(bot, user, channel, args):
    """Usage: !auth user password """

    if len(args.split()) == 2:
	name,passwd = args.split()
	passwd = hashlib.sha1(passwd).hexdigest()
        conn = sqlite3.connect(bot.nickname + ".db")
        cursor = conn.cursor()
        cursor.execute("SELECT name,passwd,level FROM users where name = '%s'" % name)
	comp = cursor.fetchone()
	if comp:
	    if str(comp[1]) == passwd:
		bot.authenticated[getHostmask(user)] = comp[2]
		cursor.execute("UPDATE users SET hostmask = '%s' WHERE name = '%s'" % (getHostmask(user),name))
		conn.commit()
		bot.say(channel,"welcome %s (%s)" % (str(comp[0]),getHostmask(user)))
		bot.log("%s was authenticated sucessfully" % str(comp[0]))

	    else:
		bot.say(channel,"wrong password")

	else:
	    bot.say(channel,"sorry, u're not on the userbase")

    else:
        bot.say(channel, "Usage error.  See 'help auth'")

def privcommand_useradd(bot,user,channel,args):
    """Usage: !useradd user password"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
	if len(args.split()) == 2:
	    user,passwd = args.split()
	    conn = sqlite3.connect(bot.nickname + ".db")
	    cursor = conn.cursor()
	    cursor.execute("INSERT INTO users VALUES (NULL,?,?,'1',NULL,NULL)",(unicode(user.lower(),'utf-8'),hashlib.sha1(passwd).hexdigest()))
	    conn.commit()
	    bot.say(channel, "%s added with passwd (%s) " % (user.lower(),password))

	else:
    	    bot.say(channel, "Usage error.  See 'help useradd'")

def privcommand_sethost(bot, user, channel, args):
    """Usage: !sethost password newhostmask """

    lvl = bot.checkValidHostmask(user)
    if lvl:
	if len(args.split()) == 2:
	    passwd,newhm = args.split()
	    passwd = hashlib.sha1(passwd).hexdigest()
	    conn = sqlite3.connect(bot.nickname + ".db")
	    cursor = conn.cursor()
    	    cursor.execute("SELECT name,level FROM users where passwd = '%s'" % passwd)
	    comp = cursor.fetchone()
	    if comp:
		del bot.authenticated[getHostmask(user)]
		bot.authenticated[newhm] = str(comp[1])
        	cursor.execute("UPDATE users SET hostmask = '%s' WHERE name = '%s'" % (newhm,str(comp[0])))
    	        conn.commit()
		bot.say(channel,"ok, %s hostmask updated to %s" % (str(comp[0]),newhm))
	    else: 
		bot.say(channel,"wrong password")

    else:
	bot.say(channel, "sorry, u're not authenticated yet")

def privcommand_checkauth(bot, user, channel, args):
    """Usage: !checkauth """

    lvl = bot.checkValidHostmask(user)
    if lvl:
	bot.say(channel, "authenticated with level %s" % lvl)
    else:
	bot.say(channel, "sorry, u're not authenticated yet")