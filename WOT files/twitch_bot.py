from dotenv import load_dotenv
import os
import twitchio
from twitchio.ext import commands
import SessionStats_class
import Player_class
import datetime
import time
import asyncio
import nest_asyncio

load_dotenv() # load enviroment variables

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token = os.getenv("TMI_TOKEN"), prefix='!', initial_channels=['Waikin_'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    # announce that bot has arrived
    async def event_channel_joined(self, channel: twitchio.Channel):
        await channel.send("/me HAS ARRIVED!")


    # basic hello command
    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')


    async def session_calculations(self, session: SessionStats_class.SessionStatsTracker, initial_player: Player_class.Player, channel: twitchio.Channel):

        player_now = Player_class.Player(session.server, session.user_name)
        player_now.fetchStats()
        tank_id = session.diffInBattles(initial_player, player_now)
        if tank_id:                 
            print(f"NEW battles found at {datetime.datetime.now()}")
            print(f"Tank ID with new battle is {tank_id}")
            inital_tank = initial_player.individualTank(tank_id)
            tank_now = player_now.individualTank(tank_id)
            battle_stats = session.battleStats(tank_id, inital_tank, tank_now)
            print(battle_stats)
            await channel.send(battle_stats)                 
        else:
            print(f"No new battles found at {datetime.datetime.now()}\n")


    @commands.command(name="start")
    async def session_tracking(self, ctx: commands.Context):
        
        # rewriting session stats tracker here, can't figure out a way to send messages to channel while within the while loop
        session = SessionStats_class.SessionStatsTracker("na", "waikin_reppinKL")
        initial_player = Player_class.Player(session.server, session.user_name)
        initial_player.fetchStats()
        start_msg = f"Player session stats for {session.user_name} initialized at {datetime.datetime.now()}\n"
        print(start_msg)
        await ctx.send(start_msg)

        try:
            while True:
                    time.sleep(10)
                    print("FUCKCKCK")
                    loop = asyncio.new_event_loop()
                    task = loop.create_task(self.session_calculations(session, initial_player, "waikin_"))
                    print("???????????")
                    loop.run_until_complete(task)


        except KeyboardInterrupt:
            print('Session Ended')
            #print(session.sessionStats)
            await ctx.send("Session has been ended!")

                
                



bot = Bot()
bot.run()

