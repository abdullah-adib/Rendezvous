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

def getEmbed(title, description):
    embed = discord.Embed(title=title, description=description, color=0xff00f7)
    embed.set_author(name="Rendezvous Bot", url="https://devpost.com/software/rendezvous-q6jxyi", icon_url=globals.iconURL)
    embed.set_footer(text="Data provided by ticketmaster.com")
    return embed

def getDropdownMenuEventEmbed(eventID):
    eventsrc = globals.apireq.makeTicketMasterAPICall(globals.eventToken, "/discovery/v2/events/{}".format(eventID)).result
    if eventsrc == None:
        print("error")
        return
    event = json.loads(eventsrc)
    tmp = filter2(event, 1)
    embed = getEmbed(tmp.name, tmp.toString())
    embed.set_image(url = tmp.image)
    return embed

def getDropdownMenuEventVenue(venueID):
    print(venueID)
    # eventsrc = globals.apireq.makeTicketMasterAPICall(globals.eventToken, "/discovery/v2/venues/{}".format(venueID)).result
    eventsrc = globals.apireq.makeTicketMasterAPICall(globals.eventToken, "/discovery/v2/venues/KovZpZA7AAEA").result
    if eventsrc == None:
        print("error")
        return
    event = json.loads(eventsrc)
    tmp = filter3(event, 1)
    embed = getEmbed(tmp.name, tmp.toString())
    embed.set_image(url = tmp.image)
    return embed


class Select(discord.ui.Select):
    def __init__(self, opt):
        super().__init__(placeholder="Select an event to view more details",max_values=1,min_values=1,options=opt)

    async def callback(self, interaction: discord.Interaction):
        print(self.values[0])
        if self.values[0][0] == '1':
            await interaction.response.send_message(embed = getDropdownMenuEventEmbed(self.values[0][1:]) ,ephemeral=True)
        elif self.values[0][0] == '0':
            await interaction.response.send_message(embed = getDropdownMenuEventVenue(self.values[0][1:]) ,ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, opt, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select(opt))

def filter3(x, maxEvents):
    return Filter1Element(x['name'], x['url'], '', '', x['id'], venID=x['_embedded']['venues'][0]['id'], image=x['images'][0]['url'])

# returns an array of Filter1Element
def filter2(x, maxEvents):
    return Filter1Element(x['name'], x['url'], \
        x['classifications'][0]['segment']['name'] if 'classifications' in x else None, \
        x['dates']['start']['localDate'], x['id'], x['images'][0]['url'])

# returns an array of Filter1Element
def filter1(events, maxEvents):
    return [ Filter1Element(x['name'], x['url'], \
        x['classifications'][0]['segment']['name'] if 'classifications' in x else None, \
        x['dates']['start']['localDate'], ID=x['id'], venID=x['_embedded']['venues'][0]['id']) \
        for x in events['_embedded']['events'] ][0:maxEvents]

def getDropdownMenu(filter1List, isEvent):
    opt = []
    i = 1
    if isEvent == True:
        for x in filter1List:
            opt.append(discord.SelectOption(label="{}. {}".format(i, x.name), \
                value = '1' + x.ID, emoji = globals.classToEmoji(x.classifications)))
        i = i + 1
    else:
        for x in filter1List:
            opt.append(discord.SelectOption(label="{}. {}".format(i, x.name), \
                value = '0' + x.venID, emoji = globals.classToEmoji(x.classifications)))
        i = i + 1
    print(opt)
    return SelectView(opt)

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
    ID = ''
    classifications = ''
    localDate = ''
    image = ''
    venID = ''
    def __init__(self, name, url, classifications, localDate, ID, image = '', venID = ''):
        tmp = lambda x: x if x != None else ''
        self.classifications = tmp(classifications)
        self.name = tmp(name)
        self.url = tmp(url)
        self.localDate = tmp(localDate)
        self.ID = ID
        self.image = image
        self.venID = venID
    def toString(self):
        return "{} {} {} \n {} \n\n".format(self.name, \
            globals.classToEmoji(self.classifications), "({})".format(self.localDate) if self.localDate != '' else '', \
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
        embed=discord.Embed(title="List of commands", description="Below are the possible commands than can be run by the bot. ", color=0x00ff40)
        embed.set_author(name="Rendezvous Bot ~ RDV", url="https://github.com/abdullah-adib/RU-Hacks-2022-Discord", icon_url="https://github.com/abdullah-adib/RU-Hacks-2022-Rendezvous-Discord-Bot/blob/main/assets/you.png")
        embed.add_field(name="/rdv suggest", value="-- Find random events.", inline=False)
        embed.add_field(name="/rdv city", value="-- Search for an event based on your city of choice.", inline=False)
        embed.add_field(name="/rdv date", value="-- Search for an event on a specifc date. [ YY-MM-DD ]", inline=False)
        embed.add_field(name="/rdv venue", value="-- Search for events at a specific venue.", inline=False)
        embed.set_footer(text="Want to contribute? Go to https://tinyurl.com/yckmaes3.")
        await user.send(embed=embed)
        await ctx.respond('DM\'ed {} the command list.'.format(user.mention))
    
    # suggest
    @rdv.command(description='Displays a random event.')
    async def suggest(self, ctx: ApplicationContext):
        eventsrc = globals.apireq.makeTicketMasterAPICall( globals.eventToken, "/discovery/v2/suggest").result
        if eventsrc == None:
            print("error")
            return
        event = json.loads(eventsrc)
        filterList = filter1(event, 5)
        await ctx.respond(embed = getEmbed("Suggested events", \
            printerNumbered(filterList)))
        await ctx.respond(view = getDropdownMenu(filterList, True))

    # debug
    @rdv.command(description='Debugging')
    async def debug(self, ctx: ApplicationContext):
        await ctx.respond('f00f')

    # date
    @rdv.command(description='Fetches events on a specific date.')
    async def date(self, ctx: ApplicationContext, year: Option(int, description='The target year.', min_value=1000), month: Option(int, description='The target month.', min_value=1, max_value=12), day: Option(int, description='The target day.', min_value=1, max_value=31)):
        dateStr = f"{year:04}-{month:02}-{day:02}"
        await ctx.respond(f'Fetching events on {dateStr}...')
        eventsrc = globals.apireq.makeTicketMasterAPICall2(globals.eventToken, '/discovery/v2/events', [ f'localStartDateTime={dateStr}T00:00:00,{dateStr}T11:59:59', f'sort=date,asc']).result
        if eventsrc == None:
            print("error")
            return
        event = json.loads(eventsrc)
        tmp = filter1(event, 5)
        await ctx.respond(embed = getEmbed(f"Events on {dateStr}", \
            printerNumbered(tmp)))
        await ctx.respond(view = getDropdownMenu(tmp, True))

    # venue
    @rdv.command(description='Fetches events at a venue.')
    async def venue(self, ctx: ApplicationContext, venue: Option(str, description='The venue to search.')):
        await ctx.respond(f'Fetching events at a venue matching \"{venue}\"...')
        sanitizedVenue = venue.replace(' ', '%20')
        venuessrc = globals.apireq.makeTicketMasterAPICall2(globals.eventToken, '/discovery/v2/venues', [ f'keyword={sanitizedVenue}', 'size=1', 'page=0']).result
        if venuessrc == None:
            print('error')
            return
        
        venuesJson = json.loads(venuessrc)
        if '_embedded' not in venuesJson:
            await ctx.respond(f'I can\'t find any venues matching \"{venue}\"')
            return
        
        firstVenue = venuesJson['_embedded']['venues'][0]
        venueId = firstVenue['id']
        venueName = firstVenue['name']
        venueCountry = firstVenue['country']['name']

        eventsrc = globals.apireq.makeTicketMasterAPICall2(globals.eventToken, '/discovery/v2/events', [ f'venueId={venueId}']).result
        if eventsrc == None:
            print("error")
            return
        
        event = json.loads(eventsrc)
        if '_embedded' not in event:
            await ctx.respond(f'I can\'t find any events at {venueName}, {venueCountry}')
            return
        
        filterlist = filter1(event, 5)
        tmp = printerNumbered(filterlist)
        embed=discord.Embed(title=f"Events at {venueName}, {venueCountry}", description=tmp, color=0xff00f7)
        embed.set_author(name="Rendezvous Bot", url="https://devpost.com/software/rendezvous-q6jxyi", icon_url="https://cdn.discordapp.com/icons/928825084297244692/1f3858a72bc26b3a617141acaad37a53.png")
        embed.set_footer(text="Data provided by ticketmaster.com")
        await ctx.respond(embed = embed)
        view = getDropdownMenu(filterlist, False)
        await ctx.respond(view = view)

    # city : retrives list of events in city
    @rdv.command(description='Fetches events in a particular city.')
    async def city(self, ctx: ApplicationContext, city: str):
        await ctx.respond(f'Fetching events in {city}...')
        eventsrc = globals.apireq.makeTicketMasterAPICall2(globals.eventToken, "/discovery/v2/events", ["city={}".format(city)]).result
        if eventsrc == None:
            print("error")
            return
        try:
            event = json.loads(eventsrc)
            tmp = filter1(event, 5)
            await ctx.respond(embed = getEmbed(f"Events in {city}", \
                    printerNumbered(tmp)))
            await ctx.respond(view = getDropdownMenu(tmp, True))
        except KeyError as e:
            await ctx.respond(f'No events found in {city}.')
