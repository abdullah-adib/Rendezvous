from utils.event_requester import EventRequester

iconURL = "https://cdn.discordapp.com/attachments/971866244875714575/972742833930899486/sunny.jpg"
prefix: str = ''
token: str = ''
eventToken: str = ''
apireq: EventRequester = None
__classToEmoji = { 
    'Arts & Theatre': '🎭',
    'Music': '🎶',
    'Sports': '🏀',
}

iconURL = "https://cdn.discordapp.com/attachments/971866244875714575/972742833930899486/sunny.jpg"

def classToEmoji(className):
    print(className)
    return __classToEmoji[className] if className in __classToEmoji else '🎟️'

