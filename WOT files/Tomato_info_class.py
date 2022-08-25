import requests
from operator import itemgetter

def WR(self, wins, battles):

        return str((wins/battles) * 100)

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

        # Recent stats by battles *includes battles, overall wins, wn8, and has specific tank stats
        self.recent1000 = self.recentStats["recent1000"]
        self.recent1000Tanks = {int(tank["id"]): tank for tank in self.recentStats["recent1000"]["tankStats"]} # tank_id from tomato backed is in str format
        self.recent100 = self.recentStats["recent100"]
        
        #self.recent60 = self.recentStats["recent60"] idk what 60 is
        #self.recent30 = self.recentStats["recent30"]

        # Recent stats by days
        self.recent24hr = self.recentStats["recent24hr"]
        self.recent3days = self.recentStats["recent3days"]
        self.recent7days = self.recentStats["recent7days"]
        self.recent30days = self.recentStats["recent30days"]
        self.recent60days = self.recentStats["recent60days"]

    def WR(self, wins, battles):

        return str(round(((wins/battles) * 100), 2))

    # doesnt work
    def discordRecentsString(self):

        return (f"> **24 hr Recents:** {str(self.recent24hr['overallWN8'])} wn8 | {self.WR(self.recent24hr['wins'], self.recent24hr['battles'])} % WR\n"
        f"> **3 Day Recents:** {str(self.recent3days['overallWN8'])} wn8 | {self.WR(self.recent3days['wins'], self.recent3days['battles'])} % WR\n"
        f"> **7 Day Recents:** {str(self.recent7days['overallWN8'])} wn8 | {self.WR(self.recent7days['wins'], self.recent7days['battles'])} % WR\n"
        f"> **30 Day Recents:** {str(self.recent30days['overallWN8'])} wn8 | {self.WR(self.recent30days['wins'], self.recent30days['battles'])} % WR\n"
        f"> **60 Day Recents:** {str(self.recent60days['overallWN8'])} wn8 | {self.WR(self.recent60days['wins'], self.recent60days['battles'])} % WR\n")

test = TomatoGGInfo("na", "waikin_reppinKL")

print(test.recent1000Tanks)





