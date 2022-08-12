import csv

exp_values = {}

with open("wn8exp values.csv", "r") as input:
    reader = csv.reader(input)

exp_values = {rows[0]:rows[1] for rows in reader}
print(exp_values)