import pig
import discord
import os
from discord.ext import commands
client = discord.Client()
bot =commands.Bot(command_prefix="!")
pig.play(client, bot)
client.run(os.environ['token'])
