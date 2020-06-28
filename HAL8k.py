import discord
import json
import threading
import asyncio
import substring
import random
import requests 
import os
import subprocess
import commands
from discord.ext import commands
import aiohttp
from io import BytesIO
from requests.sessions import session

client = discord.Client()
token = json.load(open('token.json'))['token']
# print(token)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$'):
        content = message.content.split('$')[1]
        if 'open' in content and 'bay' in content and 'doors' in content :
            await message.channel.send("I can\'t do that for you, {}.".format(message.author.mention))
        else:
            await message.channel.send('That is not a recognized command. \nPlease type `$HELP` or `$man HAL` for further information.')
        
        
        
client.run(token);
