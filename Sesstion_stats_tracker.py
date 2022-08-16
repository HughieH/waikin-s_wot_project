import json
import Player_class
import datetime
import time
import expectedValueWN8

def diffInBattles(player_before: Player_class.Player, player_after: Player_class.Player):
    
    tank_id = False
    
    for tank in player_before.allTankBattles:
        if player_before.allTankBattles[tank]["battles"] != player_after.allTankBattles[tank]["battles"]:
            tank_id = tank # tank_id integer for tank that has new battle

    return tank_id

def battleStats(tank_id, stats_before, stats_after):
    diffInStats = {parameter: stats_after[parameter] - stats_before[parameter] for parameter in stats_before}
    wn8 = expectedValueWN8.calculateWn8(tank_id, diffInStats['damage_dealt'], diffInStats['dropped_capture_points'], 
        diffInStats['frags'], diffInStats['spotted'], diffInStats['wins'] * 100)
    
    if diffInStats["wins"]:
        result = "BATTLE WON"
    else:
        result = "BATTLE LOST"
    return f"{result}\n Damge: {diffInStats['damage_dealt']}\n WN8: {wn8}\n Kills: {diffInStats['frags']}\n Exp: {diffInStats['xp']}\n"

def sessionStats():
    pass

def sessionStatsTracker(server, user_name):
    
    total_wins = total_battles = 0

    with open("session_stats.json", "r+") as session_stats:
        session_file = json.load(session_stats)

    initial_player = Player_class.Player(server, user_name)
    initial_player.fetchStats()
    print(f"Player seesion stats for {user_name} initialized at {datetime.datetime.now()}\n")
    
    try:
        while True:

            time.sleep(10)
            player_now = Player_class.Player(server, user_name)
            player_now.fetchStats()
            tank_id = diffInBattles(initial_player, player_now)
            if tank_id == False:
                print(f"No new battles found at {datetime.datetime.now()}\n")
            else:
                print(f"NEW battles found at {datetime.datetime.now()}")
                print(f"Tank ID with new battle is {tank_id}")
                inital_tank = initial_player.individualTank(tank_id)
                tank_now = player_now.individualTank(tank_id)
                print(battleStats(tank_id, inital_tank, tank_now))
                
                
                # last-battle updated stats, this keeps the session specific to new battles
                initial_player = player_now


    except KeyboardInterrupt:
        print('Session Ended')


sessionStatsTracker("na", "waikin_reppinKL")