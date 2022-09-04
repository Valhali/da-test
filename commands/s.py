from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord
import TenGiphPy

class S(BaseCommand): 

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        #if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            #await message.channel.send("Komenda testowa - musisz być modkiem by z niej korzystać")
           # return

        try:
            await message.delete()
        except :
            pass         
            
        
        cmd = message.content[len(settings.COMMAND_PREFIX)+1:].strip()
        if not cmd : return
        
        id = re.findall(r'\d+',cmd )[0]
        if not id: return
        
        m = await message.channel.fetch_message(int(id))
        if not m : return
        
        
        for attr in dir(m):
            if hasattr( m, attr ):
                print( "m.%s = %s" % (attr, getattr(m, attr)))
        #embed = discord.Embed(color=0x00ffFF)
        #embed.title = cmd
        #embed.description = i[1]
        #if gif: 
        #    embed.set_image( url=gif)
        #pprint(m)               
        #await message.channel.send(embed=embed)
        #await m.reply(cmd[19:]) #, mention_author=False
        