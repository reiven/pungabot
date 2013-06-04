# -*- coding: utf-8 -*-
import sys

aliases = {}


def init(config):
    dbCursor.execute("SELECT alias, command FROM ALIASES")
    for alias, command in dbCursor.fetchall():
        config_alias(alias, command)


def config_alias(alias, command):
    mod = globals()
    aliases[alias] = command
    mod['command_' + alias] = \
        lambda *args: run_alias(alias, *args)


def set_alias(bot, alias, command):
    config_alias(alias, command)

    dbCursor.execute("DELETE FROM aliases WHERE alias = ?", (alias,))
    dbCursor.execute("INSERT INTO aliases VALUES (?, ?)", (alias, command))


def clear_alias(bot, alias):
    del aliases[alias]
    del bot.factory.ns['module_alias.py'][0]['command_' + alias]
    dbCursor.execute("DELETE FROM aliases WHERE alias = ?", (alias,))


def get_alias(bot, alias):
    return aliases[alias]


def get_all_aliases(bot):
    return aliases.keys()


def run_alias(alias, bot, user, channel, args):
    cmd = get_alias(bot, alias) + " " + args
    bot._command(user, channel, cmd)


def command_alias(bot, user, channel, args):
    """Manage aliases"""
    if not args:
        return bot.say(channel, 'Available aliases: %s' %
            str(", ".join(get_all_aliases(bot)))
        )
    else:
        args = args.split(" ")
        aname = args[0]
        rest = " ".join(args[1:])
        if not rest:
            try:
                clear_alias(bot, aname)
            except KeyError:
                return bot.say(channel, '%s, no encontre el alias %s'
                    % (getNick(user), aname))
            return bot.say(channel, '%s, alias %s borrado'
                    % (getNick(user), aname))
        else:
            if aname == 'alias':
                return bot.say(channel, '%s, no gracias'
                    % (getNick(user),))
            set_alias(bot, aname, rest)
            return bot.say(channel, '%s, alias %s agregado'
                    % (getNick(user), aname))