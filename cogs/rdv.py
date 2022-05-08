from datetime import datetime
from random import choices
from typing import List
from unicodedata import name
import discord
import globals
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option, \
    OptionChoice

from utils.debugging_constants import DebuggingConstants
from utils.event_requester import EventRequest

# returns an array of Filter1Element
def filter1(events, maxEvents):
    return [ Filter1Element(x['name'], x['url'], \
        x['classifications'][0]['segment']['name'] if 'classifications' in x else None, \
        x['dates']['start']['localDate']) \
        for x in events['_embedded']['events'] ][0:maxEvents ]

def printer(filter1List):
    labels = []
    for x in filter1List:
        labels.append(x.toString())
    return "".join(labels)

def printerNumbered(filter1List):
    labels = []
    tmp = []
    for x in filter1List:
        labels.append(x.toString())
    labels = list(enumerate(labels))
    for x in labels:
        tmp.append("{}. {}".format(x[0] + 1, x[1]))
    return "".join(tmp)

class Filter1Element:
    name = ''
    url = ''
    classifications = ''
    localDate = ''
    def __init__(self, name, url, classifications, localDate):
        tmp = lambda x: x if x != None else ''
        self.classifications = tmp(classifications)
        self.name = tmp(name)
        self.url = tmp(url)
        self.localDate = tmp(localDate)
    def toString(self):
        return "{} {} ({}) \n {} \n\n".format(self.name, \
            globals.classToEmoji(self.classifications), self.localDate, \
            self.url)

class RDV(commands.Cog):
    # Initialize the cog
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    rdv = SlashCommandGroup(name = 'rdv', \
        description = 'Rendezvous commands.', \
        guild_ids=DebuggingConstants.guild_ids)

    # COMMANDS
    # help: DM help to user
    @rdv.command(description='Show the list of commands.')
    # @rdv.command(description='Shows a description on how to use this bot.')
    async def help(self, ctx: ApplicationContext):
        user = ctx.interaction.user
        await user.send(globals.usage)
        await ctx.respond('DM\'ed {} the command list.'.format(user.mention))

    # suggest
    @rdv.command(description='Displays a random event.')
    async def suggest(self, ctx: ApplicationContext):
        eventsrc = globals.apireq.makeTicketMasterAPICall( globals.eventToken, "/discovery/v2/suggest").result
        if eventsrc == None:
            print("error")
            return
        event = json.loads(eventsrc)
        tmp = printerNumbered(filter1(event, 5))
        embed=discord.Embed(title="Suggested events", description=tmp, color=0xff00f7)
        embed.set_author(name="Rendezvous Bot", url="https://devpost.com/software/rendezvous-q6jxyi", icon_url="https://cdn.discordapp.com/icons/928825084297244692/1f3858a72bc26b3a617141acaad37a53.png")
        embed.set_footer(text="Data provided by ticketmaster.com")
        await ctx.respond(embed = embed)

    # debug
    @rdv.command(description='Debugging')
    async def debug(self, ctx: ApplicationContext):
        await ctx.respond('f00f')

    # date
    @rdv.command(description='Fetches events on a specific date.')
    async def date(self, ctx: ApplicationContext, year: Option(int, description='The target year.', min_value=1000), month: Option(int, description='The target month.', min_value=1, max_value=12), day: Option(int, description='The target day.', min_value=1, max_value=31)):
        dateStr = f"{year:04}-{month:02}-{day:02}"
        eventsrc = globals.apireq.makeTicketMasterAPICall2(globals.eventToken, '/discovery/v2/events', [ f'localStartDateTime={dateStr}T00:00:00,{dateStr}T11:59:59', f'sort=date,asc']).result
        if eventsrc == None:
            print("error")
            return
        event = json.loads(eventsrc)
        tmp = printerNumbered(filter1(event, 5))
        embed=discord.Embed(title=f"Events on {dateStr}", description=tmp, color=0xff00f7)
        embed.set_author(name="Rendezvous Bot", url="https://devpost.com/software/rendezvous-q6jxyi", icon_url="https://cdn.discordapp.com/icons/928825084297244692/1f3858a72bc26b3a617141acaad37a53.png")
        embed.set_footer(text="Data provided by ticketmaster.com")
        await ctx.respond(embed = embed)
