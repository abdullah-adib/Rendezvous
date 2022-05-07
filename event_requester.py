import time

class EventRequest():
    url = None
    result = None
    ageLimit = None
    def __init__(self, url, result, ageLimit):
        self.url = url
        self.result = result
        self.ageLimit = ageLimit

class EventRequester:
    requestCache = {}
    def makeTicketMasterAPICall(token, requestStr):

        if requestStr in requestStr:
            # update cached result if its old

            

        conn = http.client.HTTPSConnection("app.ticketmaster.com")
        conn.request("GET", "{}?apikey={}".format(requestStr, token))
        res = conn.getresponse()
        return res.read().decode('utf-8')

