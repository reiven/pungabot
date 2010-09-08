import datetime
import random

def handle_userJoined(bot,user,channel):
    """Someone Joined, lets salute him"""

    if random.randrange(10) < 8:
	return

    tarde = datetime.time(13,00)
    noche = datetime.time(20,00)
    manha = datetime.time(07,00)
    ahora = datetime.datetime.now().time()

    # custom ahora, for debug
    #ahora = datetime.time(07,00)

    if ahora > noche or ahora < manha:
	hi = random.choice(['wenas noches','ah we.. ','nas noches','welcome back','nas noches','guten abend','uh'])
        return bot.say(channel,'%s, %s' % (getNick(user),hi))

    elif ahora > tarde:
	hi = random.choice(['guten tag','estas son horas de llegar?','wenas tardes','doctor!','alo','apa!'])
        return bot.say(channel,'%s, %s' % (getNick(user),hi))

    else:
	hi = random.choice(['morning','wen dia','madrugando eh?','que temprano!!!','guten morgen','si! q tal'])
        return bot.say(channel,'%s, %s'  % (getNick(user),hi))

