import requests

all_tank_stats = ((requests.get("https://api.worldoftanks.com/wot/tanks/stats/?application_id=bd644ca5adf8dc631b1598528a4b7fc1&account_id=" + "1027186831")).json())\
["data"]["1027186831"]

#Test_dict = {}
#Test_dict.update(overall_info)

print(all_tank_stats)