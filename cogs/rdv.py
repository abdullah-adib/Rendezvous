from random import choices
from typing import List
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option, OptionChoice

from guilds import DebuggingConstants

class RDV(commands.Cog):
    # Initialize the cog
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    rdv = SlashCommandGroup(name = 'rdv', \
        description = 'Rendezvous commands.', guild_ids=DebuggingConstants.guild_ids)

    usage = """
        ```
        LIST OF COMMANDS
        1.  /rdv help                     -- Show this help message.
        2.  /rdv [team]                   -- Show events about a sports team.
        3.  /rdv random                   -- Show a random event.
        4.  /rdv price {free/paid}        -- Filter events by price.
        5.  /rdv place {indoors/outdoors} -- Filter events by place.
        6.  /rdv top {int index}          -- Show the events with the most interest.
        7.  /rdv upcoming {int index}     -- Show upcoming events.
        8.  /rdv new                      -- Show new events.
        9.  /rdv {date (mm-dd)}           -- Show events on a particular date.
        10. /rdv sub {event name}         -- subscribe to an event.
        ```
    """

    # COMMANDS
    # help: DM help to user
    @rdv.command(description='Show the list of commands.')
    # @rdv.command(description='Shows a description on how to use this bot.')
    async def help(self, ctx: ApplicationContext):
        user = ctx.interaction.user
        await user.send(self.usage)
        await ctx.respond('DM\'ed {} the command list.'.format(user.mention))

    # random
    @rdv.command(description='Fetches a random event.')
    async def random(self, ctx: ApplicationContext):
        await ctx.respond('Fetching random event... (This is just a test.)')

    @rdv.command(description='Fetches events based on whether it is free or paid.')
    async def price(self, ctx: ApplicationContext, price_type: Option(str, choices=['free', 'paid'])):
        await ctx.respond(f'Fetching {price_type} events...')
