# Imports
from typing import List
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext

from guilds import DebuggingConstants

# RDV cog class
class RDV(commands.Cog):

     # Initialize the cog
     def __init__(self, bot: commands.Bot):
          self.bot = bot

     rdv = SlashCommandGroup(name='rdv', description='Rendezvous commands.', guild_ids=DebuggingConstants.guild_ids)

     # random
     @rdv.command(description='Fetches a random event.')
     async def random(self, ctx: ApplicationContext):
          await ctx.respond('Fetching random event... (This is just a test.)')
