# Imports
from asyncio.windows_events import NULL
from distutils.log import error
import os
from unicodedata import name
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='/')

@bot.command(name='ping')
async def ping(ctx: commands.Context):
    await ctx.reply('Pong!')

@bot.event
async def on_ready():
    print('Bot has started!')

token: str = os.environ.get('BOT_TOKEN')
if token is None:
    print('Bot token is missing! Please check environment variables!')
else:
    bot.run(token)