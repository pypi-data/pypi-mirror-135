# Discode
Discode is an asynchronous Python API wrapper for the Discord REST and Gateway API. This project was inspired by [Discord.py](https://github.com/rapptz/discord.py) and may contain similar functioning.

### Basic Example Usage
```py
import discode

client = discode.Client()

# the coroutine under the decorator
# can have any name you wish to use
@client.on_event("ready")
async def ready():
    print(f"{client.user} is ready!")

@client.on_event("message")
async def message(message: discode.Message):
    content = message.content
    if content.startswith("?hi"):
        await message.channel.send("Hiii!!!")

client.start("YOUR-TOKEN-HERE")
```