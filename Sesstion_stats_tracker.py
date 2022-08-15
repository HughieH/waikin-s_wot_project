import json
import Player_class
import datetime
import time

before = {18497: 83, 57681: 3, 15905: 69, 17473: 167, 14673: 72, 44289: 154}
after = {18497: 83, 57681: 5, 15905: 69, 17473: 167, 14673: 77, 44289: 154}


def diffInBattles(player_before, player_after):
    
    tank_id = False
    
    for tank in player_before.allTankBattles:
        if player_before.allTankBattles[tank] != player_after.allTankBattles[tank]:
            tank_id = tank # tank_id integer for tank that has new battle

    return tank_id




def sessionStatsTracker(server, user_name):
    
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
                print(f"NEW battles found at {datetime.datetime.now()}\n")
                print(f"Tank ID with new battle is {tank_id}")


    except KeyboardInterrupt:
        print('Session Ended')


sessionStatsTracker("na", "waikin_reppinKL")