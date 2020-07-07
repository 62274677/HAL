import os
import discord
import json
import hal_commands

from io import BytesIO
from requests.sessions import session
from logging import Logger
# import required classes

from PIL import Image, ImageDraw, ImageFont

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
msg = ' '
# print(token)


# Define this to work with python
# const MESSAGE_CHAR_LIMIT = 2000;

# const splitString = (string, prepend = '', append = '') => {
#   if (string.length <= MESSAGE_CHAR_LIMIT) {
#     return [string];
#   }

#   const splitIndex = string.lastIndexOf('\n', MESSAGE_CHAR_LIMIT - prepend.length - append.length);
#   const sliceEnd = splitIndex > 0 ? splitIndex : MESSAGE_CHAR_LIMIT - prepend.length - append.length;
#   const rest = splitString(string.slice(sliceEnd), prepend, append);

#   return [`${string.slice(0, sliceEnd)}${append}`, `${prepend}${rest[0]}`, ...rest.slice(1)];
# };

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$'):
        content = message.content.split('$')[1]
        if content.upper() == 'HELP' or ('man' in content and 'HAL' in content):
            message_type = 'message'
            msg = 'Commands are limited to '
        elif 'open' in content and 'bay' in content and 'doors' in content :
            message_type = 'message'
            msg = "I'm sorry, {}, I'm afraid I can't do that.".format(message.author.mention)
        elif content == 'embed':
            message_type = 'embed'
        elif content.startswith('ccdc calendar'):
            if content == 'ccdc calendar embed':
                msg = hal_commands.generate_ccdc_calendar()[1]
                message_type = 'embed'
            else:
                msg = hal_commands.generate_ccdc_calendar()[1]
                hal_commands.image_writer(msg)
                # await message.channel.send(file=discord.File("image.png"))
                message_type = 'image'
                file = discord.File("image.png")

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
                exampleEmbed.add_field(name='Regular field title', value= '\n```'+msg+'```')
                await message.channel.send(embed=exampleEmbed)
                await message.channel.send('\n`'+msg+'`')
            elif message_type == 'image':
                await message.channel.send(file=discord.File("image.png"))
                os.remove(file.filename)
            else:
                print("silence is golden")
        except Exception as e:
            await message.channel.send(e)
            Logger.error(e,e)
            
        
client.run(token)
