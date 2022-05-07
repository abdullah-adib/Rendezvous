import calendar;
import time;

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
        self.ageLimit = ageLimit
        self.deltaTime = deltaTime

class EventRequester:
    requestCache = {}
    def __makeTicketMasterAPICall(token, requestStr):
        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        conn.request("GET", "{}?apikey={}".format(requestStr, token))
        res = conn.getresponse()
        return res.read().decode('utf-8')

    def makeTicketMasterAPICall(self, token, requestStr, deltaTime = 3600):
        now = getUnixTime()
        ret = None
        # check cache
        if requestStr in self.requestCache:
            cached = self.requestCache[requestStr]
            if now - cached.timeCreated > cached.deltaTime:
                # update old cached results
                self.requestCache[requestStr] = EventRequest(requestStr, \
                    self.__makeTicketMasterAPICall(token), now, deltaTime)
        else:
            self.requestCache[requestStr] = EventRequest(requestStr, \
                    self.__makeTicketMasterAPICall(token), now, deltaTime)


        return self.requestCache[requestStr]
    ret if ret != None else self.requestCache[requestStr]

