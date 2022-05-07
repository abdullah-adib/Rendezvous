from random import choices
from typing import List
import discord
import globals
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option, OptionChoice

from utils.guilds import DebuggingConstants

class RDV(commands.Cog):
    # Initialize the cog
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    rdv = SlashCommandGroup(name = 'rdv', \
        description = 'Rendezvous commands.', guild_ids=DebuggingConstants.guild_ids)

    # COMMANDS
    # help: DM help to user
    @rdv.command(description='Show the list of commands.')
    # @rdv.command(description='Shows a description on how to use this bot.')
    async def help(self, ctx: ApplicationContext):
        user = ctx.interaction.user
        await user.send(self.usage)
        await ctx.respond('DM\'ed {} the command list.'.format(user.mention))

    # suggest
    @rdv.command(description='Displays a random event.')
    async def suggest(self, ctx: ApplicationContext):
        eventsrc = globals.apireq.makeTicketMasterAPICall(\
            globals.eventToken, "/discovery/v2/suggest")
        print(eventsrc.result)
        await ctx.respond('f00f')

    # random
    @rdv.command(description='Fetches a random event.')
    async def random(self, ctx: ApplicationContext):
        await ctx.respond('Fetching random event... (This is just a test.)')

    @rdv.command(description='Fetches events based on whether it is free or paid.')
    async def price(self, ctx: ApplicationContext, price_type: Option(str, choices=['free', 'paid'])):
        await ctx.respond(f'Fetching {price_type} events...')
