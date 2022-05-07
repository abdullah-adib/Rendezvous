#  ================ Imports ==================
from asyncio.windows_events import NULL
from discord.ext import commands
from distutils.log import error
from dotenv import load_dotenv
from unicodedata import name
import discord
import os
# ===========================================

load_dotenv() # Load the dotenv file

prefix: str = os.environ.get('PREFIX') # Get the prefix from the dotenv file
bot = commands.Bot(command_prefix=prefix)

# Test command
# @bot.command(name='test')
# async def ping(ctx: commands.Context):
#     await ctx.reply('bot working!')



# ============= Bot is running =============
@bot.event
async def on_ready():
    print('Bot has started!')

token: str = os.environ.get('BOT_TOKEN') # Get the bot token and check if it is valid
if token is None:
    print('Bot token is missing! Please check environment variables!')
else:
    bot.run(token)
# ===========================================