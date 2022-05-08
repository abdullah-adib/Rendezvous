import os
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
from cogs.rdv import RDV
import http.client
from utils.event_requester import EventRequester
import os
import globals

# set global state
# load environment variables from .env
load_dotenv()
globals.prefix = os.environ.get('PREFIX')
globals.token = os.environ.get('BOT_TOKEN')
globals.eventToken = os.environ.get('TICKETMASTER_TOKEN')
globals.apireq = EventRequester()
# prefix: str = os.environ.get('PREFIX')
# token: str = os.environ.get('BOT_TOKEN')
# eventToken: str = os.environ.get('TICKETMASTER_TOKEN')

# http://app.ticketmaster.com?&apikey=

# globals.apireq.makeTicketMasterAPICall2('euPCM1HnI3S8NWM68MCzLKR5mwicWGhv', '/discovery/v2/events', [ 'startDateTime=2022-06-07T00:00:00Z'])
# exit

# EventRequester example usage
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # default update time is 1 hour
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # this will be cached 
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest", 0) # change the update time to 0 seconds
# a = ereq.makeTicketMasterAPICall(eventToken, "/discovery/v2/suggest") # this will be updated
# exit()

# create bot
bot = commands.Bot(command_prefix=globals.prefix)

# emits a message when the bot is ready
@bot.event
async def on_ready():
    print('Bot has started!')
# start bot
if globals.token is None:
    print('Bot token is missing! Please check environment variables!')
else:
    bot.add_cog(RDV(bot))
    bot.run(globals.token)
