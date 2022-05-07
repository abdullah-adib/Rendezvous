from distutils.log import error
from dotenv import load_dotenv
from unicodedata import name
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.rdv import RDV
import http.client
from event_requester import EventRequester
import os
import time

# load environment variables from .env
load_dotenv()
prefix: str = os.environ.get('PREFIX')
token: str = os.environ.get('BOT_TOKEN')
eventToken: str = os.environ.get('TICKETMASTER_TOKEN')

# EventRequester example usage
# ereq = EventRequester()
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # default update time is 1 hour
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # this will be cached 
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest", 0) # change the update time to 0 seconds
# time.sleep(2)
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # this will be updated
# exit()

# create bot
bot = commands.Bot(command_prefix=prefix)

# emits a message when the bot is ready
@bot.event
async def on_ready():
    print('Bot has started!')
# start bot
if token is None:
    print('Bot token is missing! Please check environment variables!')
else:
    bot.add_cog(RDV(bot))
    bot.run(token)
