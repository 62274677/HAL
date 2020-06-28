import discord
import json
import hal_commands

from io import BytesIO
from requests.sessions import session
from logging import Logger

#---currently unused---
# import threading
# import asyncio
# import substring
# import random
# import requests 
# import os
# import subprocess
# from discord.ext import commands
# import aiohttp



client = discord.Client()
token = json.load(open('token.json'))['token']
message_type = "" #message, embed, both, undefined
msg = ""
# print(token)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$'):
        content = message.content.split('$')[1]
        if content.upper() == 'HELP' or ('man' in content and 'HAL' in content):
            message_type = 'message'
            msg = ':no:'
        elif 'open' in content and 'bay' in content and 'doors' in content :
            message_type = 'message'
            msg = "I'm sorry, {}, I'm afraid I can't do that.".format(message.author.mention)
        elif content == 'embed':
            message_type = 'embed'
        elif content == 'ccdc calendar':
            msg = generate_ccdc_calendar(); #not implemented
            await message.channel.send(msg)
            message_type = 'embed'
        else:
            message_type = 'message'
            msg = 'That is not a recognized command. \nPlease type `$HELP` or `$man HAL` for further information.'
        
        #Send message or embed
        try:
            if message_type == 'message':
                await message.channel.send(msg)
            elif message_type == 'embed':
                exampleEmbed =  discord.Embed(colour = 0x0099ff, title = 'Some title', url = 'https://discord.js.org/')
                exampleEmbed.set_footer(text='Some footer text here', icon_url='https://i.imgur.com/wSTFkRM.png')
                exampleEmbed.add_field(name='Regular field title', value= '\n```'+hal_commands.table_test()+'```')
                await message.channel.send(embed=exampleEmbed)
                msg = str(hal_commands.table_test())
                await message.channel.send('\n`'+msg+'`')
        except Exception as e:
            await message.channel.send(e)
            Logger.error(e,e)
            
        
client.run(token);
