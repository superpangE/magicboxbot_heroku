import pig
import discord
import os
client = discord.Client()
bot =commands.Bot(command_prefix="!")
pig.play(client, bot)
client.run(os.environ['token'])
