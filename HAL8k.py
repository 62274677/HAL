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
        msg = ' '
        message_type = "" #message, embed, both, undefined
        max_characters = 2000
        max_width = 100
        ccdc_calendar = ''
        
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
                ccdc_calendar = hal_commands.generate_ccdc_calendar()
                msg = ccdc_calendar[0]
                hal_commands.image_writer(msg)
                
                meeting = hal_commands.find_next_meeting(ccdc_calendar[4])
                ccdcEmbed = discord.Embed(color = 0x0099ff, title = 'Upcoming CCDC Meeting (CLICK HERE FOR REMINDERS)',url = ccdc_calendar[1])
                ccdcEmbed.add_field('Next meeting: ' + meeting[0][1])
                
                message_type = 'embed'
            elif content == 'ccdc calendar msg':
                msg = hal_commands.generate_ccdc_calendar()[0]
                message_type = 'message'
            else:
                msg = hal_commands.generate_ccdc_calendar()[0]
                hal_commands.image_writer(msg)
                # await message.channel.send(file=discord.File("image.png"))
                message_type = 'image'
                

        else:
            message_type = 'message'
            msg = 'That is not a recognized command. \nPlease type `$HELP` or `$man HAL` for further information.'
        
        #Send message or embed
        try:
            if message_type == 'message':
                msg_arr = []
                msg_length = len(msg)
                if msg_length > max_characters:
                    if msg.find('\n')< max_width:
                        i=0
                        while i < msg_length-1:
                        # for i in range(msg_length-1):
                            start = i
                            i+= max_characters-1 if i+(max_characters-1) <= msg_length-1 else msg_length-1-i #make i the ceiling of max characters or message length
                            line_break = msg.rfind('\n',start,i)
                            print('last index' + str(i) + '\n last newline' + str(line_break))
                            if line_break<i and line_break > 0:
                                i = line_break
                            msg_arr.append(msg[start:i])
                            i+=1
                        for m in msg_arr:
                            await message.channel.send('\n```'+m+'```')
                        msg = "```Error: Message exceeded {0} characters and was therefore split into multiple messages.```".format(max_characters)
                    else:
                        hal_commands.image_writer(msg)
                        
                        await message.channel.send(file=discord.File("image.png"))
                        os.remove("image.png")
                        msg = "Message exceeded {0} characters and {1} characters per line.".format(max_characters, max_width)
                        
                await message.channel.send('\n`'+msg+'`')
            
            elif message_type == 'embed':
                
                # exampleEmbed =  discord.Embed(colour = 0x0099ff, title = 'Some title', url = 'https://discord.js.org/')
                # exampleEmbed.set_footer(text='Some footer text here', icon_url='https://i.imgur.com/wSTFkRM.png')
                # exampleEmbed.add_field(name='Regular field title', value= '\n```'+msg+'```')
                
                # await message.channel.send(embed=exampleEmbed)
                # await message.channel.send('\n`'+msg+'`')
            elif message_type == 'image':
                file = ''
                await message.channel.send(file=discord.File("image.png"))
                os.remove("image.png")
            else:
                print("silence is golden")
        except Exception as e:
            await message.channel.send(e)
            Logger.error(e,e)
            
        
client.run(token)
