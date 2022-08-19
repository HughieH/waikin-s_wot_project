from twitchio.ext import routines
import asyncio


@routines.routine(seconds=5.0, iterations=5)
async def hello(arg: str):
    print(f'Hello {arg}!')

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(hello.start("gamer"))
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

