prefix = ''
token = ''
eventToken = ''
usage = """
```
LIST OF COMMANDS
1.  /rdv help                     -- Show this help message.
2.  /rdv [team]                   -- Show events about a sports team.
3.  /rdv suggest                  -- Show a random event.
4.  /rdv price {free/paid}        -- Filter events by price.
5.  /rdv place {indoors/outdoors} -- Filter events by place.
6.  /rdv top {int index}          -- Show the events with the most interest.
7.  /rdv upcoming {int index}     -- Show upcoming events.
8.  /rdv new                      -- Show new events.
9.  /rdv {date (mm-dd)}           -- Show events on a particular date.
10. /rdv sub {event name}         -- subscribe to an event.
```
"""
apireq = None
__classToEmoji = { 
    'Arts & Theatre': '🎭',
    'Music': '🎶',
    'Sports': '🏀',
}

def classToEmoji(className):
    print(className)
    return __classToEmoji[className] if className in __classToEmoji else '🎟️'
