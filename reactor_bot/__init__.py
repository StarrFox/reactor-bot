#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.5.4'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

import discord
from discord.ext import commands

from reactor_bot.cogs.poll import Poll

prefixes = []
for capitalization in ('Poll', 'poll', 'POLL'):
    prefixes.append(capitalization + ':')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes))


@bot.event
async def on_ready():
    message = 'Logged in as: %s' % bot.user
    separator = '━' * len(message)
    print(separator, message, separator, sep='\n')
    await bot.change_presence(game=discord.Game(name='poll:help'))


# since discord.py doesn't allow for commands with no name,
# (poll: foo) we have to process them manually in that case
@bot.event
async def on_message(message):
    context = await bot.get_context(message)

    if context.prefix:
        if context.command:
            await bot.process_commands(message)
        else:
            await Poll.reaction_poll(message)


@bot.event
async def on_message_edit(before, after):
    if any(reaction.me for reaction in before.reactions):
        try:
            await before.clear_reactions()
        except discord.errors.Forbidden:
            return
    await on_message(after)
