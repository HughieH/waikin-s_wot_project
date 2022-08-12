def dpg_target(initial_dpg, initial_games):
    
    if initial_dpg >= 5000:
        return("DPG is already 5k!")
    else:
        initial_total_damage= initial_dpg * initial_games
        for i in range(10):
            i += 1
            final_total_damage = 5000 * (i + initial_games)
            total_damage_needed = final_total_damage - initial_total_damage
            print(total_damage_needed)
            damage_needed = total_damage_needed / i
            print("The average damage needed in " + str(i) + " games is " + str(damage_needed))

