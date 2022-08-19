from twitchio.ext import routines



@routines.routine(seconds=5.0, iterations=5)
async def hello(arg: str):
    print("hehehehehee")
    print(f'Hello {arg}!')

hello.start('World')
