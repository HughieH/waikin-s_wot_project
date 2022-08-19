import json
import Player_class
import datetime
import time
import expectedValueWN8

class SessionStatsTracker:

    def __init__(self, server: str, user_name: str) -> None:
        
        self.server = server
        self.user_name = user_name
        self.totalbattles = self.total_wins = 0
        self.sessionStats = {}

    def diffInBattles(self, player_before: Player_class.Player, player_after: Player_class.Player):
    
        tank_id = False
    
        for tank in player_before.allTankBattles:
            if player_before.allTankBattles[tank]["battles"] != player_after.allTankBattles[tank]["battles"]:
                tank_id = tank # tank_id integer for tank that has new battle

        return tank_id
    
    def battleStats(self, tank_id, stats_before, stats_after):
        diffInStats = {parameter: stats_after[parameter] - stats_before[parameter] for parameter in stats_before}
        wn8 = expectedValueWN8.calculateWn8(tank_id, diffInStats['damage_dealt'], diffInStats['dropped_capture_points'], 
            diffInStats['frags'], diffInStats['spotted'], diffInStats['wins'] * 100)
        
        if diffInStats["wins"]:
            result = "BATTLE WON"
        else:
            result = "BATTLE LOST"
        
        time = datetime.datetime.now()
        battleStats = {time.strftime("%c"): {"Tank_ID": tank_id, "Damage": diffInStats['damage_dealt'], "WN8": round(wn8, 2), "Kills": diffInStats['frags'],
            "Exp": diffInStats['xp']}}
        

        self.sessionStats.update(battleStats)
        
        return f"{result}\nDamge: {diffInStats['damage_dealt']}\nWN8: {round(wn8, 2)}\nKills: {diffInStats['frags']}\nExp: {diffInStats['xp']}\n"
    
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
                    print(self.battleStats(tank_id, inital_tank, tank_now))
                    
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