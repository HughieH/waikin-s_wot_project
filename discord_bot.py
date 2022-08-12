import discord
import sys
import Player_class

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
            overall_wn8 = player.username + " has an overall wn8 of " + str(player.overallAccountWn8)
            await message.channel.send(overall_wn8)
            print("Success!!")

        else:
            await message.channel.send("Wrong format")

sys.path.insert(0, '/Users/wanho/Desktop')
import Discord_bot_API_keys


# Insert bot token here
client.run(Discord_bot_API_keys.Token)  