# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite3
import hashlib
import string

######################################################################
# auth : authenticate to the bot. this will auto-update your hostmask

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
		bot.reloadUsers()
		bot.say(channel,"welcome %s (%s)" % (str(comp[0]),getHostmask(user)))
		bot.log("%s was authenticated sucessfully" % str(comp[0]))

	    else:
		bot.say(channel,"wrong password")

	else:
	    bot.say(channel,"sorry, u're not on the userbase")

    else:
        bot.say(channel, "Usage error.  See 'help auth'")

######################################################################
# adduser : this will add a new user to the db, setting him a password

def privcommand_adduser(bot,user,channel,args):
    """Usage: !useradd user password"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
	if len(args.split()) == 2:
	    user,passwd = args.split()
	    conn = sqlite3.connect(bot.nickname + ".db")
	    cursor = conn.cursor()
	    cursor.execute("INSERT INTO users VALUES (NULL,?,?,'1',NULL,NULL)",(unicode(user.lower(),'utf-8'),hashlib.sha1(passwd).hexdigest()))
	    conn.commit()
	    bot.reloadUsers()
	    bot.say(channel, "%s added with passwd (%s) " % (user.lower(),password))

	else:
    	    bot.say(channel, "Usage error.  See 'help adduser'")

######################################################################
# addbot : the main difference between users and bots is lack of password (by now) 
#          for the bots, and the hostmask need to be precise to auto-op them

def privcommand_addbot(bot,user,channel,args):
    """Usage: !addbot botname hostmask"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
	if len(args.split()) == 2:
	    botname,hostmask = args.split()
	    conn = sqlite3.connect(bot.nickname + ".db")
	    cursor = conn.cursor()
	    cursor.execute("INSERT INTO users VALUES (NULL,?,NULL,'4',?,NULL)",(unicode(botname.lower(),'utf-8'),hostmask))
	    conn.commit()
	    bot.reloadUsers()
	    bot.say(channel, "%s added with hostmask (%s) " % (botname.lower(),hostmask))

	else:
    	    bot.say(channel, "Usage error.  See 'help addbot'")

def privcommand_delbot(bot,user,channel,args):
    """Usage: !delbot [password] botname"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
	if len(args.split()) == 2:
	    passwd, botname = args.split()
	    passwd = hashlib.sha1(passwd).hexdigest()
	    conn = sqlite3.connect(bot.nickname + ".db")
	    cursor = conn.cursor()
	    cursor.execute("SELECT name FROM users where passwd = '%s'" % passwd)
    	    comp = cursor.fetchone()
            if comp:
	        cursor.execute("SELECT name,level,hostmask FROM users WHERE name = '%s'" % botname)
		dele = cursor.fetchone()
		if dele and str(dele[1]) == "4":
	    	    cursor.execute("DELETE FROM users WHERE name = '%s'" % botname)
		    conn.commit()
		    del bot.authenticated[str(dele[2])]
		    bot.say(channel, "%s deleted ok" % (botname.lower()))
		else:
		    bot.say(channel, "%s is not a valid bot" % (botname.lower()))

	else:
    	    bot.say(channel, "Usage error.  See 'help delbot'")

######################################################################
# set: [host]  change hostmask (allowing you use wildcards)
#      [email] set email

def privcommand_sethost(bot, user, channel, args):
    """Usage: !sethost password newhostmask """

    if bot.checkValidHostmask(user):
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
		bot.reloadUsers()
		bot.say(channel,"ok, %s hostmask updated to %s" % (str(comp[0]),newhm))
	    else: 
		bot.say(channel,"wrong password")

    else:
	bot.say(channel, "sorry, u're not authenticated yet")

######################################################################
### check : commands for verification of auto-auth

def privcommand_check(bot, user, channel, args):
    """Usage: !check [auth/level] """

    if args and bot.checkValidHostmask(user):
        if args.lower() == "auth":
	    bot.say(channel, "you are authenticated ok")

        if args.lower() == "level":
	    bot.say(channel, "your actual level is %s" % bot.checkValidHostmask(user))
    else:
        bot.say(channel, "wrong usage, see help")
