""" The main driver file of the Discord bot
"""

# load the environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
TOKEN = os.environ["YEETBOT_TOKEN"]

from discord.ext import commands

prefix = "!"
bot = commands.Bot(command_prefix=prefix)

bot.load_extension("cogs.filter")
bot.load_extension("cogs.overlay")
bot.load_extension("cogs.settings")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
