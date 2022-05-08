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

    def __makeTicketMasterAPICallSingle(self, token, requestStr):
        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        tmp = "{}?apikey={}".format(requestStr, token)
        conn.request("GET", tmp)
        res = conn.getresponse()
        return res.read().decode('utf-8')

    def __makeTicketMasterAPICallMulti(self, token, requestStr):
        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        tmp = "{}?{}".format(requestStr, token)
        conn.request("GET", tmp)
        res = conn.getresponse()
        return res.read().decode('utf-8')

    def __newEventRequest(self, token, requestStr, now, deltaTime, apicaller):
        self.requestCache[requestStr] = EventRequest(requestStr, \
            apicaller(token, requestStr), now, deltaTime)

    def makeTicketMasterAPICall(self, token, requestStr, deltaTime = 3600):
        now = getUnixTime()
        ret = None
        # check cache
        if requestStr in self.requestCache:
            print('value was cached')
            cached = self.requestCache[requestStr]
            if cached.result == None:
                self.__newEventRequest(token, requestStr, now, deltaTime, \
                    self.__makeTicketMasterAPICallSingle)
            else:
                # update delta time if needed
                if cached.deltaTime != deltaTime:
                    print("updating delta time")
                    cached.deltaTime = deltaTime
                if now - cached.timeCreated > cached.deltaTime:
                    # update old cached results
                    print('cache is old, updating ...')
                    self.__newEventRequest(token, requestStr, now, deltaTime, \
                        self.__makeTicketMasterAPICallSingle)
        else:
            print('value was not cached')
            self.__newEventRequest(token, requestStr, now, deltaTime, \
                self.__makeTicketMasterAPICallSingle)
        return self.requestCache[requestStr]

    def makeTicketMasterAPICall2(self, token, requestStr, requestStrParams, deltaTime = 3600):
        newtoken = requestStrParams
        newtoken.append(token)
        tmp = []
        for x in newtoken[0:-1]:
            tmp.append(x)
            tmp.append('&')
        tmp.append('apikey=')
        tmp.append(newtoken[-1])
        newToken = "".join(tmp)
        now = getUnixTime()
        ret = None
        # check cache
        if requestStr in self.requestCache:
            print('value was cached')
            cached = self.requestCache[requestStr]
            if cached.result == None:
                self.__newEventRequest(newToken, requestStr, now, deltaTime, \
                    self.__makeTicketMasterAPICallMulti)
            else:
                # update delta time if needed
                if cached.deltaTime != deltaTime:
                    print("updating delta time")
                    cached.deltaTime = deltaTime
                if now - cached.timeCreated > cached.deltaTime:
                    # update old cached results
                    print('cache is old, updating ...')
                    self.__newEventRequest(newToken, requestStr, now, deltaTime, \
                        self.__makeTicketMasterAPICallMulti)
        else:
            print('value was not cached')
            self.__newEventRequest(newToken, requestStr, now, deltaTime, \
                self.__makeTicketMasterAPICallMulti)
        return self.requestCache[requestStr]

