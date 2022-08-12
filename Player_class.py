import requests
import expectedValueWN8
import averageExpectedOverallValueWN8
from operator import itemgetter


class Player:

    def __init__(self, server, user_name):
        
        self.username = user_name
        self.playerServer = server.lower()
        #API error handling 
        
        if self.playerServer == "na":
            player_info = ((requests.get("https://api.worldoftanks.com/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0] # DICT value keys for userID
        else: 
            player_info = ((requests.get("https://api.worldoftanks." + self.playerServer + "/wot/account/list/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&search=" + self.username)).json())\
            ["data"][0]
        
        self.userID = player_info["account_id"]

#---------------------------------------------------------------------------------------------------------------------------------------------------------
        # overall stats
        if self.playerServer == "na":
            overall_info = ((requests.get("https://api.worldoftanks.com/wot/account/info/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&account_id=" + str(self.userID))).json())\
            ["data"][str(self.userID)] # DICT value keys for overall player info
        else: 
            overall_info = ((requests.get("https://api.worldoftanks." + self.playerServer + "/wot/account/info/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&account_id=" + str(self.userID))).json())\
            ["data"][str(self.userID)]

        self.wgRating = overall_info["global_rating"]
        self.overallStats = {}
        self.overallStats.update(overall_info["statistics"]["all"])
        self.totalBattles = self.overallStats["battles"]
        self.winRate = round((self.overallStats["wins"] / self.totalBattles) * 100, 2)
        self.dpg = round(self.overallStats["damage_dealt"] / self.totalBattles)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
        # getting tank-specific stats from WG API
        if self.playerServer == "na":
            # lists of all the tanks a player has nested in a dictionary
            self.allTankStats = ((requests.get("https://api.worldoftanks.com/wot/tanks/stats/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&account_id=" + str(self.userID) +\
                "&fields=-in_garage%2C+-frags%2C+-max_frags%2C+-team%2C+-stronghold_defense%2C+-globalmap%2C+-clan%2C+-stronghold_skirmish%2C+-company%2C+-regular_team%2C+-account_id%2C+-max_xp"\
                )).json())["data"][str(self.userID)] # dictionaries nested in list
        
        else:
            self.allTankStats = ((requests.get("https://api.worldoftanks." + self.playerServer + "/wot/tanks/stats/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&account_id=" + str(self.userID) +\
                "&fields=-in_garage%2C+-frags%2C+-max_frags%2C+-team%2C+-stronghold_defense%2C+-globalmap%2C+-clan%2C+-stronghold_skirmish%2C+-company%2C+-regular_team%2C+-account_id%2C+-max_xp"\
                )).json())["data"][str(self.userID)] 

        # number of tanks a player has ACCORDING to the WOT API, may not be the same once cross-referenced with the XVM expected values JSON file
        self.numberOfTanks = len(self.allTankStats)
        # list of all tank wn8 values, list is empty in constructor but gets filled when the tankWN8 method is called
        self.allTankWN8 = []
        self.skippedTankID = []
        self.tankWN8()
        self.overallWn8 = self.overallWN8()
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------   
    # calculate wn8 for each individual tank
    def tankWN8(self):
        
        # for loop iterates through each tank's random battles, variable randBattleStats is a nested dictionary containing tank stats
        for i in self.allTankStats:
            randBattleStats = i["all"]
            if randBattleStats["battles"] == 0:
                pass
            else:
                try:
                    # Calculate wn8, parameters are (id, avgDamage, avgDef, avgFrag, avgSpots, winrate)
                    wn8 = expectedValueWN8.calculateWn8(i["tank_id"], (randBattleStats["damage_dealt"]/randBattleStats["battles"]), (randBattleStats["dropped_capture_points"]/randBattleStats["battles"])\
                    , (randBattleStats["frags"]/randBattleStats["battles"]), (randBattleStats["spotted"]/randBattleStats["battles"]), ((randBattleStats["wins"]/randBattleStats["battles"]) * 100))
                    
                    tank_stat = {"Tank ID": i["tank_id"], "Tank WN8": wn8, "Tank Battles": randBattleStats["battles"]}
                    self.allTankWN8.append(tank_stat)
                    #print(tank_stat)
                    #print(len(self.allTankWN8))
                # in the event that tank_id from WG API cannot be found in JSON file list, tank is skipped
                except AttributeError:
                    self.skippedTankID.append(i["tank_id"])
                    print(str(i["tank_id"]) + " was skipped!")
                    pass
                    

#---------------------------------------------------------------------------------------------------------------------------------------------------------   
    # calculate overall wn8 by using overall stats and weighted averages of expected values
    def overallWN8(self):
        
        overall_stats_input = []
        total_damage = total_def = total_frag = total_spot = total_wr = 0
        
        #print("-------------------------------------------------")
        #print("All Tank ID and Battles from WOT API for the Player: ")
        #print("-------------------------------------------------")
        
        for i in self.allTankStats:
            tank_values = {"Tank ID": i["tank_id"], "Battles": i["all"]["battles"]}
            #print(tank_values)
            overall_stats_input.append(tank_values)
            total_damage += i["all"]["damage_dealt"]
            total_def += i["all"]["dropped_capture_points"]
            total_frag += i["all"]["frags"]
            total_spot += i["all"]["spotted"]
            total_wr += (i["all"]["wins"]) * 100

        #print("-------------------------------------------------")

        return averageExpectedOverallValueWN8.calculateOverallWn8(overall_stats_input, total_damage, total_def, total_frag, total_spot, total_wr)

#---------------------------------------------------------------------------------------------------------------------------------------------------------           
    # calculated overall wn8 of a player by weighted averages
    def overallWeightedWn8(self):
        
        # calculates the overall wn8 of a player, done by averaging wn8 per tank weighted by number of games per tank
        sum_of_damage_times_battles = 0
        total_battles = 0
        for i in self.allTankStats:
            sum_of_damage_times_battles += (i["Tank WN8"] * i["Tank Battles"])
            total_battles += i["Tank Battles"]
        
        print("Total battles from cross-referencing JSON: " + str(total_battles))
        return (sum_of_damage_times_battles / total_battles)

#---------------------------------------------------------------------------------------------------------------------------------------------------------   
    def sortedListOfTanks(self):

        return sorted(self.allTankWN8, key = itemgetter("Tank Battles"), reverse = True)




    def print(self):
        print(self.username)
        print(self.playerServer)
        print("User ID is: " + str(self.userID))
        #print("WG rating is: " + str(self.wgRating))
        print("Total battles is: " + str(self.totalBattles))
        #print("Overall win rate is " + str(self.winRate))
        #print("Overall dpg is " + str(self.dpg))
        #print("Number of tanks is: " + str(self.numberOfTanks))
        #print("Number tanks:")
        #print(len(self.allTankStats))
        print("Overall wn8 is: " + str(self.overallWN8()))
        print("-------------------------------------------------")
        print("Sorted list of Tanks: ")
        for i in self.sortedListOfTanks():
            print(i)
        print("-------------------------------------------------")
        print("-------------------------------------------------")
        print("Unsorted list of Tanks: ")
        for i in self.allTankWN8:
            print(i)
        print("-------------------------------------------------")




test = Player("na", "waikin_reppinKL")
test.print()