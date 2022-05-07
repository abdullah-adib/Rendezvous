from distutils.log import error
import os
from unicodedata import name
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.rdv import RDV

# load environment variables from .env
load_dotenv()
prefix: str = os.environ.get('PREFIX')
token: str = os.environ.get('BOT_TOKEN')

# create bot
bot = commands.Bot(command_prefix=prefix)

# BASIC COMMANDS

# @bot.command(name = 'ping')
# async def ping(ctx: commands.Context):
#     await ctx.reply('Pong!')

@bot.event
async def on_ready():
    print('Bot has started!')

# @bot.event
# async def on_message(message):
#     print('f00f')
#     # if message.content == 'test':
#     await message.channel.send('Testing 1 2 3')
#     await bot.process_commands(message)


# start bot
if token is None:
    print('Bot token is missing! Please check environment variables!')
else:
    bot.add_cog(RDV(bot))
    bot.run(token)
