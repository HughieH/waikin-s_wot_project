import json
import Player_class
import datetime
import time
import expectedValueWN8
import Color_icon_class

class SessionStatsTracker:

    def __init__(self, server: str, user_name: str):
        
        # load all_tank_data.json file, this is a dictionary of all tank information (e.g. tank name, tier, etc. ), key is based on Tank ID
        self.allTankopediaData = (json.load(open("all_tank_data.json")))["data"]
        self.server = server
        self.user_name = user_name
        self.totalbattles = self.total_wins = 0
        self.sessionStats = {}

    # finds if there is a difference in battles between two player classes
    def diffInBattles(self, player_before: Player_class.Player, player_after: Player_class.Player):
    
        tank_id = False
    
        for tank in player_before.allTankBattles:
            if player_before.allTankBattles[tank]["battles"] != player_after.allTankBattles[tank]["battles"]:
                tank_id = tank # tank_id integer for tank that has new battle

        return tank_id
    
    # finds the difference in stats between two players fir the individual tank
    def twitchBattleStats(self, tank_id, stats_before, stats_after):
        
        # dict comprehension
        diffInStats = {parameter: stats_after[parameter] - stats_before[parameter] for parameter in stats_before}
        
        wn8 = expectedValueWN8.calculateWn8(tank_id, diffInStats['damage_dealt'], diffInStats['dropped_capture_points'], 
            diffInStats['frags'], diffInStats['spotted'], diffInStats['wins'] * 100)
        wn8_color_icon = Color_icon_class.ColorIcon(wn8)
        tank_name = self.allTankopediaData[str(tank_id)]["name"]
        
        if diffInStats["wins"]:
            result = "BATTLE WON 🥇"
        else:
            result = "BATTLE LOST 💀"
        
        
        time = datetime.datetime.now()
        battleStats = {time.strftime("%c"): {"Tank_ID": tank_id, "Tank_name": tank_name, "Damage": diffInStats['damage_dealt'], "WN8": int(wn8), "Kills": diffInStats['frags'],
            "Exp": diffInStats['xp'], "Win": diffInStats["wins"]}}
        
        self.sessionStats.update(battleStats)
        
        # string message output in twitch chat
        return f"{tank_name} -> {result} || Damge: {diffInStats['damage_dealt']} || WN8: {int(wn8)} {wn8_color_icon} \
        || Kills: {diffInStats['frags']} || Exp: {diffInStats['xp']}"
    
    # prototype version of session tracking using while loop and keyboard interrupt to end event loop
    def startSessionTracking(self):

        initial_player = Player_class.Player(self.server, self.user_name)
        initial_player.fetchStats()
        print(f"Player session stats for {self.user_name} initialized at {datetime.datetime.now()}\n")

        try:
            while True:

                time.sleep(10)
                player_now = Player_class.Player(self.server, self.user_name)
                player_now.fetchStats()
                tank_id = self.diffInBattles(initial_player, player_now)
                if tank_id:
                    
                    print(f"NEW battles found at {datetime.datetime.now()}")
                    print(f"Tank ID with new battle is {tank_id}")
                    inital_tank = initial_player.individualTank(tank_id)
                    tank_now = player_now.individualTank(tank_id)
                    print(self.twitchBattleStats(tank_id, inital_tank, tank_now))
                    
                    # last-battle updated stats, this keeps the session specific to new battles
                    initial_player = player_now

                # no change in battle
                else:
                    print(f"No new battles found at {datetime.datetime.now()}\n")

        except KeyboardInterrupt:
            print('Session Ended')
            print(self.sessionStats)

#test = SessionStatsTracker("na", "waikin_reppinKL")
#test.startSessionTracking()