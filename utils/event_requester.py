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
    requestCache = None

    def __init__(self):
        self.requestCache = {}

    def __makeTicketMasterAPICall(self, token, requestStr):
        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        conn.request("GET", "{}?apikey={}".format(requestStr, token))
        res = conn.getresponse()
        return res.read().decode('utf-8')

    def __newEventRequest(self, token, requestStr, now, deltaTime):
        self.requestCache[requestStr] = EventRequest(requestStr, \
            self.__makeTicketMasterAPICall(token, requestStr), now, deltaTime)

    def makeTicketMasterAPICall(self, token, requestStr, deltaTime = 3600):
        now = getUnixTime()
        ret = None
        # check cache
        if requestStr in self.requestCache:
            print('value was cached')
            cached = self.requestCache[requestStr]
            if cached.result == None:
                self.__newEventRequest(token, requestStr, now, deltaTime)
            else:
                # update delta time if needed
                if cached.deltaTime != deltaTime:
                    print("updating delta time")
                    cached.deltaTime = deltaTime
                if now - cached.timeCreated > cached.deltaTime:
                    # update old cached results
                    print('cache is old, updating ...')
                    self.__newEventRequest(token, requestStr, now, deltaTime)
        else:
            print('value was not cached')
            self.__newEventRequest(token, requestStr, now, deltaTime)
        return self.requestCache[requestStr]

