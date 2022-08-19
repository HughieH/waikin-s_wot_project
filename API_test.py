from twitchio.ext import routines


@routines.routine(hours=1)
async def hello():
    print('Hello World!')

@hello.before_routine
async def hello_before():
    print('I am run first!')


hello.start()
print("hello")
print(type(hello.start()
))