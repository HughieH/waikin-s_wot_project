import json
import Player_class
import datetime
import time
import expectedValueWN8
import Color_icon_class
import SessionStats_DB
import Tomato_info_class

class SessionStatsTracker:

    def __init__(self, server: str, user_name: str):
        
        # load all_tank_data.json file, this is a dictionary of all tank information (e.g. tank name, tier, etc. ), key is based on Tank ID
        self.allTankopediaData = (json.load(open("all_tank_data.json")))["data"]
        # instance variables assigned to self variables
        self.server = server
        self.user_name = user_name
        self.totalbattles = self.total_wins = 0
        self.lastBattle: str # call method to fill string message
        self.compareQBMsg: dict # 3 key-value pairs
        self.scoreAgainstQB = {"Waikin": 0, "QuickyBaby": 0}
        self.sessionStats = {}

    # Helper function that finds if there is a difference in battles between two player classes -> result of this function used in battleStats
    def diffInBattles(self, player_before: Player_class.Player, player_after: Player_class.Player):
    
        tank_id = False
    
        for tank in player_before.allTankBattles:
            if player_before.allTankBattles[tank]["battles"] != player_after.allTankBattles[tank]["battles"]:
                tank_id = tank # tank_id integer for tank that has new battle

        # returns tank_id that has a new battle
        return tank_id
    
    # Helper function compares tank specific damage, wn8, kills, and spots, between player 1 and QB's 1000 day recents

    def compareToQB(self, tank_id, damage_me, wn8_me, kills_me):
        
        qb = Tomato_info_class.TomatoGGInfo("eu", "Quickfingers")
        qbTankStats = qb.recent1000Tanks[tank_id] # tomato tank stats, key is tank id (int), value is dictionary of stats
        waikinPnt = qbPnt = 0
        
        if qbTankStats["dpg"] > damage_me: qbPnt += 1
        if qbTankStats["dpg"] < damage_me: waikinPnt += 1
        if qbTankStats["wn8"] > wn8_me: qbPnt += 1
        if qbTankStats["wn8"] < wn8_me: waikinPnt += 1
        if qbTankStats["kpg"] > kills_me: qbPnt += 1
        if qbTankStats["kpg"] < kills_me: waikinPnt += 1
        
        self.scoreAgainstQB["Waikin"] += waikinPnt
        self.scoreAgainstQB["QuickyBaby"] += qbPnt

        self.compareQBMsg = {"compare_msg": f"""
        Over the last 1000 battles in the {qbTankStats['name']}, QB on AVERAGE does {qbTankStats['dpg']} damage, {qbTankStats['wn8']} wn8, 
        and {qbTankStats['kpg']} kills || Waikin did {damage_me} damage, {wn8_me} wn8, and {kills_me} kills.
        """, "current_waikin_point": waikinPnt, "current_qb_point": qbPnt}
        

    # finds the difference in stats between two players objects for the individual tank, we get tank_id from diffInBattles helper function
    def battleStats(self, tank_id, stats_before: Player_class.Player.individualTank, stats_after: Player_class.Player.individualTank):
        
        # dict comprehension, diffInStats dict now contains tank stats for individual battles
        diffInStats = {parameter: stats_after[parameter] - stats_before[parameter] for parameter in stats_before}
        
        # calculate wn8 and assign tank name
        wn8 = expectedValueWN8.calculateWn8(tank_id, diffInStats['damage_dealt'], diffInStats['dropped_capture_points'], 
            diffInStats['frags'], diffInStats['spotted'], diffInStats['wins'] * 100)
        wn8_color_icon = Color_icon_class.ColorIcon(wn8)
        tank_name = self.allTankopediaData[str(tank_id)]["name"]
        
        if diffInStats["wins"]:
            result = "BATTLE WON 🥇"
        else:
            result = "BATTLE LOST 💀"
        
        time = datetime.datetime.now()
        
        self.compareToQB(tank_id, diffInStats['damage_dealt'], int(wn8), diffInStats['frags'])

        # update session instance variable dict object
        battleStats = {time.strftime("%c"): {"Tank_ID": tank_id, "Tank_name": tank_name, "Damage": diffInStats['damage_dealt'], "WN8": int(wn8), "Kills": diffInStats['frags'],
            "Exp": diffInStats['xp'], "Win": diffInStats["wins"]}}
        self.sessionStats.update(battleStats)

        # update DB
        insert = SessionStats_DB.insertBattle(time.strftime("%c"), tank_id, tank_name, diffInStats['damage_dealt'], 
            int(wn8), diffInStats['frags'], diffInStats['xp'], diffInStats["wins"])
        SessionStats_DB.connect(insert, "session_stats")
        
        # string message assigned to self.LastBattle
        # why am I not returning the string? It's because I want to make the string available to the object I guess...
        self.lastBattle = f"{tank_name} -> {result} || Damge: {diffInStats['damage_dealt']} || WN8: {int(wn8)} {wn8_color_icon.colorWN8()} \
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
                    self.battleStats(tank_id, inital_tank, tank_now)
                    print(self.lastBattle)
                    
                    # last-battle updated stats, this keeps the session specific to new battles
                    initial_player = player_now

                # no change in battle
                else:
                    print(f"No new battles found at {datetime.datetime.now()}\n")

        except KeyboardInterrupt:
            print('Session Ended')
            print(self.sessionStats)

test = SessionStatsTracker("na", "waikin_reppinKL")
test.compareToQB()