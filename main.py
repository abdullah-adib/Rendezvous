# Imports
import os
import discord

from discord.ext import commands
from discord.commands import ApplicationCommand, ApplicationContext
from dotenv import load_dotenv

from cogs.rdv import RDV
from guilds import DebuggingConstants

load_dotenv()

bot = commands.Bot(command_prefix='/')

@bot.command(name='ping')
async def ping(ctx: commands.Context):
    await ctx.reply('Pong!')

@bot.event
async def on_ready():
    print('Bot has started!')

@bot.slash_command(name='hi', description='Say hi!', guild_ids=DebuggingConstants.guild_ids)
async def hi(ctx: ApplicationContext):
    await ctx.respond('Hi!')

token: str = os.environ.get('BOT_TOKEN')
if token is None:
    
    print('Bot token is missing! Please check environment variables!')
else:
    bot.add_cog(RDV(bot=bot))
    bot.run(token)