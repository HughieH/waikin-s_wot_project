import requests
from operator import itemgetter

class TomatoGGInfo:

    def __init__(self, server, user_name):
        
        self.username = user_name
        self.playerServer = server.lower()
        
        # find account ID using WG's API
        if self.playerServer == "na":
            account_id = ((requests.get("https://api.worldoftanks.com/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0]["account_id"] # DICT value keys for userID
        else:
            account_id = ((requests.get("https://api.worldoftanks." + self.playerServer + "/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0]["account_id"]
        
        self.accountID = account_id

        # tomato.gg 
        if self.playerServer == "na":
            self.tomatoInfo = (requests.get(f"https://tomatobackend.herokuapp.com/api/player/com/{str(self.accountID)}")).json() #
        else:
            self.tomatoInfo = (requests.get(f"https://tomatobackend.herokuapp.com/api/player/{(self.playerServer).upper()}/{str(self.accountID)}")).json()
        
        self.recentStats = self.tomatoInfo["recents"]

test = TomatoGGInfo("asia", "waikinboom")
print(test.recentStats)




