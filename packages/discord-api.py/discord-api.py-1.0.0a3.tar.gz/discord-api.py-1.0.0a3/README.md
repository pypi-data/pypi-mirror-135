# discord-api.py
![PyPI](https://img.shields.io/pypi/v/discord-api.py) ![download](https://img.shields.io/pypi/dm/discord-api.py) [![Python 3.8 Tests](https://github.com/tuna2134/discord-api.py/actions/workflows/py38-test.yml/badge.svg?branch=main)](https://github.com/tuna2134/discord-api.py/actions/workflows/py38-test.yml)

## introduction

This is discord api wrapper.

Easy to create a bot

## setup

```bash
discord-api setup main
```

## More fast

If you are not using windows and have installed cpython. I recommend using this.

```bash
pip install discord-api.py[speed]
```

## extension

If you want to create extention module.

Please do like this name.

`discord-api-{name}`

## low wrapper

If you want to use low wrapper, please watch [this](https://github.com/tuna2134/discord-api.py/blob/main/discord_api/low/README.md).

## sample

```python
from discord_api import Client, Command

client = Client(log = False)

client.add_command(Command("ping", "pong."))

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_interaction(i):
    await i.send("Pong!", True)

client.run("token")
```

## license

Watch a `LICENSE`!

## support

[Discord server](https://discord.gg/VpBs4zGC3z)

![discord](https://discord.com/widget?id=912542431185100862&theme=dark")
