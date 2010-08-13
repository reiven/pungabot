import random

def command_bola8(bot,user,channel,args):
    """show eight-ball answer"""

    if args:
	#eightball = ["As I see it, yes","It is certain","It is decidedly so","Most likely","Outlook good","Signs point to yes","Without a doubt","Yes","Yes - definitely","You may rely on it","Reply hazy, try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
	eightball = ['como patada ninja','seh, a pleno','sin duda','tal como lo veo, si', 'apa! sisi','seguro!','decididamente si','..bastante','claro','y.. apunta a que si','sin duda','sale','sisisi,si!','si, definitivamente','tan cierto como la ley de la gravedad','lo que?','wtf??','no entiendo','la verdad q ni idea','nusep','estas seguro que queres saber?','no podria afirmarlo','ignorance is bliss','no estoy seguro','uhm es medio rantesco, no se','ni siquiera lo pienses','mi respuesta es NO','nah, ni ahi','ni en pedo','uhmmmmmmmmmmm', 'el dia que los natas vuelen..','estas hablando del fffffassssoooooooo?']
	return bot.say(channel, '%s' %  random.choice(eightball))

    else:
	return bot.say(channel, 'que queres preguntar, %s?' % getNick(user))