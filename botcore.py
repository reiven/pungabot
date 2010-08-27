# -*- coding: utf-8 -*-

"""Bot core"""

# Copyright 2010 federico reiven
# License: GPL v3
# For further info, see COPYING file

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer, threads
from twisted.python import rebuild

from types import FunctionType

import os, sys
import string
import urllib
import logging
import re
import fnmatch
from util import pyfiurl
from pysqlite2 import dbapi2 as sqlite3


# line splitting
import textwrap

__pychecker__ = 'unusednames=i, classattr'

log = logging.getLogger("bot")

class CoreCommands(object):
    def command_echo(self, user, channel, args):
        self.say(channel, "%s: %s" % (user, args))

    def privcommand_ping(self, user, channel, args):
        self.say(channel, "%s: My current ping is %.0fms" % (self.factory.getNick(user), self.pingAve*100.0))

    def privcommand_rehash(self, user, channel, args):
        """Reload modules. Usage: rehash [debug]"""

	lvl = self.checkValidHostmask(user)
	if lvl and lvl > 4:
            try:
                # rebuild core & update
                log.info("rebuilding %r" % self)
                rebuild.updateInstance(self)

                self.factory._loadmodules()

            except Exception, e:
                self.say(channel, "Rehash error: %s" % e)
                log.error("Rehash error: "+e)
            else:
                self.say(channel, "Rehash OK")
                log.info("Rehash OK")
	else:
	    log.debug("%s tried priveleged !rehash command" % self.factory.getNick(user))

    def privcommand_join(self, user, channel, args):
        """Usage: join <channel>[@network] [password] - Join the specified channel"""

	lvl = self.checkValidHostmask(user)
	if not lvl or lvl < 4:
            return

        password = None
        # see if we have multiple arguments
        try:
            args, password = args.split(' ', 1)
        except ValueError, e:
            pass

        # see if the user specified a network
        try:
            newchannel, network = args.split('@', 1)
        except ValueError, e:
            newchannel, network = args, self.network.alias
        try:
            bot = self.factory.allBots[network]
        except KeyError:
            self.say(channel, "I am not on that network.")
        else:
            log.debug("Attempting to join channel %s", newchannel)
            if newchannel in bot.network.channels:
                self.say(channel, "I am already in %s on %s." % (newchannel, network))
                log.debug("Already on channel %s" % channel)
                log.debug("Channels I'm on this network: %s" % bot.network.channels)
            else:
                if password:
                    bot.join(newchannel, key=password)
                    log.debug("Joined")
                else:
                    bot.join(newchannel)
                    log.debug("Joined %s" % newchannel)

    # alias of part
    def privcommand_leave(self, user, channel, args):
        """Usage: leave <channel>[@network] - Leave the specified channel"""
        self.privcommand_part(user, channel, args)

    def privcommand_part(self, user, channel, args):
        """Usage: part <channel>[@network] - Leave the specified channel"""

	lvl = self.checkValidHostmask(user)
	if not lvl or lvl < 4:
            return

        # part what and where?
        try:
            newchannel, network = args.split('@', 1)
        except ValueError, e:
            newchannel, network = args, self.network.alias

        # get the bot instance for this chat network
        try:
            bot = self.factory.allBots[network]
        except KeyError:
            self.say(channel, "I am not on that network.")
        else:
            if newchannel not in bot.network.channels:
                self.say(channel, "I am not in %s on %s." % (newchannel, network))
                self.say(channel, "I am on %s" % bot.network.channels)
            else:
                bot.network.channels.remove(newchannel)
                bot.part(newchannel)

    def privcommand_quit(self, user, channel, args):
        """Usage: logoff - Leave this network"""

	lvl = self.checkValidHostmask(user)
	if not lvl or lvl < 4:
            return

        self.quit("Working as programmed")
        self.hasQuit = 1

    def privcommand_channels(self, user, channel, args):
        """Usage: channels <network> - List channels the bot is on"""
        if not args: 
            self.say(channel, "Please specify a network")
            return
        bot = self.factory.allBots[args]
        self.say(channel, "I am on %s" % self.network.channels)

    def command_help(self, user, channel, cmnd):
        """Get help on all commands or a specific one. Usage: help [<command>]"""

        commands = []
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            commands += [(c.replace("command_", ""),ref) for c,ref in mylocals.items() if c.startswith("command_%s" % cmnd)]

        # help for a specific command
        if len(cmnd) > 0:
            for cname, ref in commands:
                if cname == cmnd:
                    helptext = ref.__doc__.split("\n", 1)[0]
                    self.say(channel, "Help for %s: %s" % (cmnd, helptext))
                    return
        # generic help
        else:
            commandlist = ", ".join([c for c, ref in commands])

            self.say(channel, "Available commands: %s" % commandlist)

    def privcommand_help(self, user, channel, cmnd):
        """Get help on all commands or a specific one. Usage: help [<command>]"""

        commands = []
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            commands += [(c.replace("privcommand_", ""),ref) for c,ref in mylocals.items() if c.startswith("privcommand_%s" % cmnd)]

        # help for a specific command
        if len(cmnd) > 0:
            for cname, ref in commands:
                if cname == cmnd:
                    helptext = ref.__doc__.split("\n", 1)[0]
                    self.say(channel, "Help for %s: %s" % (cmnd, helptext))
                    return
        # generic help
        else:
            commandlist = ", ".join([c for c, ref in commands])

            self.say(channel, "Available commands: %s" % commandlist)


class pungaBot(irc.IRCClient, CoreCommands):
    """pungaBot"""

    nickname = "pungabot"
    realname = "cookiebot"

    # send 1 msg per 1/2 sec
    lineRate = 0.5

    hasQuit = False

    # Rolling ping time average
    pingAve = 0.0

    def __init__(self, network):
        self.network = network
        self.nickname = self.network.nickname
	self.authenticated = {}

        # text wrapper to clip overly long answers
        self.tw = textwrap.TextWrapper(width=400, break_long_words=True)

        log.info("bot initialized")


    def __repr__(self):
        return 'pungaBot(%r, %r)' % (self.nickname, self.network.address)

    ###### CORE 

    def printResult(self, msg, info):
        # Don't print results if there is nothing to say (usually non-operation on module)
        if msg:
            log.debug("Result %s %s" % (msg, info))

    def printError(self, msg, info):
        log.error("ERROR %s %s" % (msg, info))

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.repeatingPing(300)
        log.info("connection made")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        log.info("connection lost:", reason)

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""

	self.reloadUsers()

        for chan in self.network.channels:
            # defined as a tuple, channel has a key
            if type(chan) == list:
                self.join(chan[0], key=chan[1])
            else:
                self.join(chan)

        log.info("joined %d channel(s): %s" % (len(self.network.channels), ", ".join(self.network.channels)))

    def pong(self, user, secs):
        self.pingAve = ((self.pingAve * 5) + secs) / 6.0

    def repeatingPing(self, delay):
        reactor.callLater(delay, self.repeatingPing, delay)
        self.ping(self.nickname)

    def say(self, channel, message, length = None):
        """Override default say to make replying to private messages easier"""
        # wrap long text into suitable fragments
        msg = self.tw.wrap(message)

        cont = False

        for m in msg:
            if cont: m = "..."+m
            self.msg(channel, m, length)
            cont = True

        return ('botcore.say', channel, message)

    def log(self, message):
        botId = "%s@%s" % (self.nickname, self.network.alias)
        log.info("%s: %s", botId, message)

    def checkValidHostmask(self,user):
	""" based in the user hostmask, check if he/it do auth. return user level"""

	for pattern, level in self.authenticated.items():
	    if fnmatch.fnmatch(self.factory.getHostmask(user),pattern):
		log.debug("pattern matched = %s" % pattern)
		return level

	return False

    def reloadUsers(self):
	# first we should get all the hostmask for the admins/bots
        conn = sqlite3.connect(self.nickname + ".db")
        cursor = conn.cursor()
	cursor.execute ("SELECT hostmask,level FROM users ORDER BY level")
	for mask in cursor:
	    if mask[0] != None:
		log.debug("debug: %s - %s" % (mask[0],mask[1]))
		self.authenticated[mask[0]] = mask[1]
	conn.close()

    ###### COMMUNICATION

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message.

        @param user: nick!user@host
        @param channel: Channel where the message originated from
        @param msg: The actual message
        """

        channel = channel.lower()
        lmsg = msg.lower()
        lnick = self.nickname.lower()
        nickl = len(lnick)

        if channel == lnick:
	    # bot private commands
    	    if msg.startswith(self.factory.config['commandchar']):
        	cmnd = msg[len(self.factory.config['commandchar']):]
        	self._privcommand(user, self.factory.getNick(user), cmnd)

        else:
	    # public direct message to the bot
            if lmsg.startswith(lnick) and len(lmsg) > nickl and lmsg[nickl] in string.punctuation:
		log.debug("they are talking to me!")
		# if a message was sent talking to the bot, use bola8 command
                msg = "!bola8 " + msg[len(self.nickname) + 1:].lstrip()

    	    if msg.startswith(self.factory.config['commandchar']):
        	cmnd = msg[len(self.factory.config['commandchar']):]
        	self._command(user, channel, cmnd)

    	    # run URL handlers
	    urls = pyfiurl.grab(msg)
	    if urls:
        	for url in urls:
            	    self._runhandler("url", user, channel, url, msg)

        # run privmsg handlers
        self._runhandler("privmsg", user, channel, msg)

    def _runhandler(self, handler, *args, **kwargs):
        """Run a handler for an event"""
        handler = "handle_%s" % handler
        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            handlers = [(h,ref) for h,ref in mylocals.items() if h == handler and type(ref) == FunctionType]

            for hname, func in handlers:
                # defer each handler to a separate thread, assign callbacks to see when they end
                # TODO: Profiling: add time.time() to callback params, calculate difference
                d = threads.deferToThread(func, self, *args, **kwargs)
                d.addCallback(self.printResult, "handler %s completed" % hname)
                d.addErrback(self.printError, "handler %s error" % hname)

    def _command(self, user, channel, cmnd):
        """Handles bot commands.

        This function calls the appropriate method for the given command.

        The command methods are formatted as "command_<commandname>"
        """
        # split arguments from the command part        
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        # core commands
        method = getattr(self, "command_%s" % cmnd, None)
        if method is not None:
            log.info("internal command %s called by %s on %s" % (cmnd, user, channel))
            method(user, channel, args)
            return

        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c,ref) for c,ref in mylocals.items() if c == "command_%s" % cmnd]

            for cname, command in commands:
                log.info("module %s called by %s on %s" % (cname, user, channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel, args)
                d.addCallback(self.printResult, "command %s completed" % cname)
                d.addErrback(self.printError, "command %s error" % cname)

    def _privcommand(self, user, channel, cmnd):
        """Handles private bot commands.

        This function calls the appropriate method for the given command.

        The command methods are formatted as "privcommand_<commandname>"
        """
        # split arguments from the command part        
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        # core commands
        method = getattr(self, "privcommand_%s" % cmnd, None)
        if method is not None:
            log.info("internal privcommand %s called by %s on %s" % (cmnd, user, channel))
            method(user, channel, args)
            return

        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c,ref) for c,ref in mylocals.items() if c == "privcommand_%s" % cmnd]

            for cname, command in commands:
                log.info("module %s called by %s on %s" % (cname, user, channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel, args)
                d.addCallback(self.printResult, "privcommand %s completed" % cname)
                d.addErrback(self.printError, "privcommand %s error" % cname)

    ### LOW-LEVEL IRC HANDLERS ###

    def irc_JOIN(self, prefix, params):
        """override the twisted version to preserve full userhost info"""

        nick = self.factory.getNick(prefix)
        channel = params[-1]

        if nick == self.nickname:
            self.joined(channel)
        else:
            self.userJoined(prefix, channel)

        if nick.lower() != self.nickname.lower():
            pass
        elif channel not in self.network.channels:
            self.network.channels.append(channel)
            self.factory.setNetwork(self.network)

    def irc_PART(self, prefix, params):
        """override the twisted version to preserve full userhost info"""

        nick = self.factory.getNick(prefix)
        channel = params[0]

        if nick == self.nickname:
            self.left(channel)
        else:
            # some clients don't send a part message at all, compensate
            if len(params) == 1: params.append("")
            self.userLeft(prefix, channel, params[1])

    def irc_QUIT(self, prefix, params):
        """QUIT-handler.

        Twisted IRCClient doesn't handle this at all.."""

        nick = self.factory.getNick(prefix)
        if nick == self.nickname:
            self.left(channel)
        else:
    	    self.userLeft(prefix, None, params[0])

    ###### HANDLERS ######

    ## ME

    def joined(self, channel):
        """I joined a channel"""
        self._runhandler("joined", channel)

    def left(self, channel):
        """I left a channel"""
        self._runhandler("left", channel)

    def noticed(self, user, channel, message):
        """I received a notice"""
        self._runhandler("noticed", user, channel, message)

    def modeChanged(self, user, channel, set, modes, args):
        """Mode changed on user or channel"""
        self._runhandler("modeChanged", user, channel, set, modes, args)

    def kickedFrom(self, channel, kicker, message):
        """I was kicked from a channel"""
        self._runhandler("kickedFrom", channel, kicker, message)

    def nickChanged(self, nick):
        """I changed my nick"""
        self._runhandler("nickChanged", nick)

    ## OTHER PEOPLE

    def userJoined(self, user, channel):
        """Someone joined"""
        self._runhandler("userJoined", user, channel)

    def userLeft(self, user, channel, message):
        """Someone left"""
        self._runhandler("userLeft", user, channel, message)

    def userKicked(self, kickee, channel, kicker, message):
        """Someone got kicked by someone"""
        self._runhandler("userKicked", kickee, channel, kicker, message)

    def action(self, user, channel, data):
        """An action"""
        self._runhandler("action", user, channel, data)

    def topicUpdated(self, user, channel, topic):
        """Save topic to maindb when it changes"""        
        self._runhandler("topicUpdated", user, channel, topic)

    def userRenamed(self, oldnick, newnick):
        """Someone changed their nick"""
        self._runhandler("userRenamed", oldnick, newnick)

    def receivedMOTD(self, motd):
        """MOTD"""
        self._runhandler("receivedMOTD", motd)

    ## SERVER INFORMATION

    def created(self, when):
        log.info(self.network.alias+" CREATED: "+when)

    def yourHost(self, info):
        log.info(self.network.alias+" YOURHOST: "+info)

    def myInfo(self, servername, version, umodes, cmodes):
        log.info(self.network.alias+" MYINFO: %s %s %s %s" % (servername, version, umodes, cmodes))

    def luserMe(self, info):
        log.info(self.network.alias+" LUSERME: "+info)
