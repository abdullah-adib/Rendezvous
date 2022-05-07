from typing import List
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext
# from guilds import DebuggingConstants

class RDV(commands.Cog):
    # Initialize the cog
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    rdv = SlashCommandGroup(name = 'rdv', \
        description = 'Rendezvous commands.')

    usage = """
    f
    """

    # COMMANDS
    # help: DM help to user
    @rdv.command(description='Shows a description on how to use this bot.')
    async def help(self, ctx: ApplicationContext):
        await ctx.interaction.user.send(self.usage)

    # random
    @rdv.command(description='Fetches a random event.')
    async def random(self, ctx: ApplicationContext):
        await ctx.respond('Fetching random event... (This is just a test.)')
