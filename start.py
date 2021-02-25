import pig
import discord
import os
client = discord.Client()
pig.play(client)
client.run(os.environ['token'])
