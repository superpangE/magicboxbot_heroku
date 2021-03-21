import pig
import discord
from discord.utils import get
import asyncio
import random
import time
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import os
import youtube_dl
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.ext import commands
# client = discord.Client()
bot =commands.Bot(command_prefix="!")
pig.play(bot)
bot.run(os.environ['token'])
