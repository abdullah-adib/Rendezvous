import calendar
import time
import http.client

def getUnixTime():
    return calendar.timegm(time.gmtime())

class EventRequest():
    url = None
    result = None
    timeCreated = None
    deltaTime = None
    def __init__(self, url, result, timeCreated, deltaTime):
        self.url = url
        self.result = result
        self.timeCreated = timeCreated
        self.deltaTime = deltaTime

class EventRequester:
    requestCache = {}
    def __makeTicketMasterAPICall(token, requestStr):
        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        conn.request("GET", "{}?apikey={}".format(requestStr, token))
        res = conn.getresponse()
        return res.read().decode('utf-8')

    def newEventRequest(self, token, requestStr, now, deltaTime):
        self.requestCache[requestStr] = EventRequest(requestStr, \
            self.__makeTicketMasterAPICall(token), now, deltaTime)

    def makeTicketMasterAPICall(self, token, requestStr, deltaTime = 3600):
        now = getUnixTime()
        ret = None
        # check cache
        if requestStr in self.requestCache:
            print('value was cached')
            cached = self.requestCache[requestStr]
            if now - cached.timeCreated > cached.deltaTime:
                # update old cached results
                print('cache is old, updating ...')
                self.newEventRequest(token, requestStr, now, deltaTime)
        else:
            print('value was not cached')
            self.newEventRequest(token, requestStr, now, deltaTime)
        return self.requestCache[requestStr]

