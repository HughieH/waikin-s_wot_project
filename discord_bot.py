import discord
import sys
import Player_class
import Comparison_class

client = discord.Client()

@client.event
async def on_ready():
    print("Bot has logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")
    
    # example !player na waikin_reppinKL
    if message.content.startswith("!player"):
        stats = message.content.split(" ")
        print(stats)
        if len(stats) == 3:
            player = Player_class.Player(stats[1], stats[2])
            overall_wn8 = player.overallDiscordAccountStats()
            await message.channel.send(overall_wn8)
            print("Success!!")
        else:
            await message.channel.send("Wrong format, please use the format !player server username. For example '!player na waikin_reppinKL'.")
    
    # example !compare waikin_reppinKL na quickfingers eu
    # Comparison("waikin_reppinKL", "na", "quickfingers", "eu")
    if message.content.startswith("!compare"):
        input = message.content.split(" ")
        print(input)
        if len(input) == 5:
            comparison = (Comparison_class.Comparison(input[1], input[2], input[3], input[4])).compareOverallStats()
            await message.channel.send(f"**__Comparison of Overall Stats:__**\n{comparison}")
            print("Success!!")
        else:
            await message.channel.send("Wrong format, please use the format !compare name1 server1 name2 server2.\
             For example '!compare waikin_reppinKL na quickfingers eu'.")

sys.path.insert(0, '/Users/wanho/Desktop')
import Discord_bot_API_keys


# Insert bot token here
client.run(Discord_bot_API_keys.Token)  