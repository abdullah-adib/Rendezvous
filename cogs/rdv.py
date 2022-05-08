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

        eventLabels = list(enumerate([ (x['name'], x['url'], x['classifications'][0]['segment']['name'] ) for x in event['_embedded']['events'] ][0:5]))
        func = lambda x: "{}. {} {}\n {}\n\n".format(x[0] + 1, x[1][0], globals.classToEmoji(x[1][2]), x[1][1])
        funcLast = lambda x: "{}. {} {}\n {}\n\n".format(x[0] + 1, x[1][0], globals.classToEmoji(x[1][2]), x[1][1])
        labels = []
        for x in eventLabels[0:-1]:
            print(func(x))
            labels.append(func(x))
        labels.append(funcLast(eventLabels[-1]))
        embed=discord.Embed(title="Suggested events", description="".join(labels), color=0xff00f7)
        embed.set_author(name="Rendezvous Bot", url="https://devpost.com/software/rendezvous-q6jxyi", icon_url="https://cdn.discordapp.com/icons/928825084297244692/1f3858a72bc26b3a617141acaad37a53.png")
        embed.set_footer(text="Data provided by ticketmaster.com")
        await ctx.respond(embed = embed)

    # debug
    @rdv.command(description='Debugging')
    async def debug(self, ctx: ApplicationContext):
        await ctx.respond('f00f')

    # date
    @rdv.command(description='Fetches events on or after a specific date.')
    async def date(self, ctx: ApplicationContext, year: Option(int, description='The target year.', min_value=0), month: Option(int, description='The target month.', min_value=1, max_value=12), day: Option(int, description='The target day.', min_value=1, max_value=31)):
        dateStr = f"{year:04}-{month:02}-{day:02}"
        eventsrc = globals.apireq.makeTicketMasterAPICall( globals.eventToken, f"/discovery/v2/events?startDateTime={dateStr}T00:00:00Z").result
        print(str(eventsrc))
        if eventsrc == None:
            print("error")
            return
        event = json.loads(eventsrc)
        embed = discord.Embed(title=f"EVENTS ON OR AFTER {year}-{month}-{day}")
        i = 0
        for x in event['_embedded']['events']:
            if i >= 5:
                break
            embed.add_field(name = "{}".format(i + 1), value = x['name'])
        await ctx.respond(embed = embed)
