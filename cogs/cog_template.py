# Imports
import discord
from discord.ext import commands

# Template cog class
class CogTemplate(commands.Cog):

     # Initialize the cog
     def __init__(self, bot: commands.Bot):
          self.bot = bot

     # Template command
     @commands.command()
     async def template(self, ctx: commands.Context):
          await ctx.send("Template command")
