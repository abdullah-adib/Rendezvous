from utils.event_requester import EventRequester


prefix: str = ''
token: str = ''
eventToken: str = ''
apireq: EventRequester = None
__classToEmoji = { 
    'Arts & Theatre': '🎭',
    'Music': '🎶',
    'Sports': '🏀',
}

def classToEmoji(className):
    print(className)
    return __classToEmoji[className] if className in __classToEmoji else '🎟️'

