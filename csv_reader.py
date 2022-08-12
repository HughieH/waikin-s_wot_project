import csv

exp_values = {}

# header is 'tank_id', 'dmg', 'frg', 'spo', 'def', 'win', 'battles', 'type', 'tier', 'tag'
# indexes: [    0        1      2      3      4      5        6         7       8      9 ]

with open("wn8exp values.csv", "r") as input:
    csv_reader = csv.reader(input)
    exp_values = {rows[0]:rows for rows in csv_reader}

# format for each key value pair
# '1': ['1', '486.793', '0.978', '1.377', '1.133', '54.914', '183381087', 'mediumTank', '5', 'R04_T-34']

#print(exp_values)
    