# -*- coding: utf-8 -*-

import pytz
#
# we can use any method inside tweepy from modules, thanks to global twapi
#

from util import pyfiurl

def showTwit(bot,where,twname,status):
    for s in status:
	bsas = pytz.timezone('America/Argentina/Buenos_Aires')
	bot.say(where, '%s: %s (%s)' % (twname,s.text.encode('utf-8'),s.created_at.replace(tzinfo=pytz.utc).astimezone(bsas).strftime("%H:%M - %d.%m.%Y")))
	urls = pyfiurl.grab(s.text.encode('utf-8'))
	if urls:
	    for url in urls:
		bot._runhandler("url", twname, where, url, ".")

def command_twitter(bot,user,channel,args):
    """show last twitter update from given user"""

    if len(args.split()) == 1:
	try:
	    status = twapi.user_timeline(args,count='1',include_rts='true')

	except: 
	    return bot.say(channel, '%s: %s is not a valid twitter user' % (getNick(user), args))

	showTwit(bot,channel,args,status)

    elif len(args.split()) == 2:
	twuser,num = args.split()

	if int(num) <= 5:
	    try:
		status = twapi.user_timeline(twuser,count=num,include_rts='true')

	    except: 
		return bot.say(channel, '%s: %s is not a valid twitter user' % (getNick(user), twuser))

	    showTwit(bot,channel,twuser,status)

	else:
	    bot.say(channel, 'sorry %s, i can only show five twits' % getNick(user))

    else:
	bot.say(channel, '%s, which user status you wanna see?' % getNick(user))

def command_twitterwho(bot,user,channel,args):
    """show twitter information about a given user"""

    if len(args.split()) == 1:
        try:
            who = twapi.get_user(screen_name=args)

        except:
            return bot.say(channel, '%s: %s is not a valid twitter user' % (getNick(user), args))

	if who.name and who.url:
	    bot.say(channel, '%s: %s (%s)' % (args,who.name.encode('utf-8'),who.url.encode('utf-8')))

	else:
	    bot.say(channel, '%s: %s' % (args,who.name.encode('utf-8')))

    else:
	return bot.say(channel, 'usage error, see !help twitterwho')

def privcommand_twupdate(bot,user,channel,args):
    """update bot status on twitter"""

    lvl = bot.checkValidHostmask(user)
    if lvl and lvl >= 3:
        if args:
	    twapi.update_status( '%s' % args )
    	    return bot.say(user, 'ok %s, status updated' % getNick(user))

	else:
	    return bot.say(user,'%s, what do you wanna post to tw?' % getNick(user))

