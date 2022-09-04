from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord
import TenGiphPy

class Rea(BaseCommand): 

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        #if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Komenda testowa - musisz być modkiem by z niej korzystać")
            return

        try:
            await message.delete()
        except :
            pass         
            
        
        cmd = message.content[len(settings.COMMAND_PREFIX)+3:].strip()
        if not cmd : return
        
        id = re.findall(r'\d+',cmd )[0]
        if not id: return
        
        emoji = cmd[19:].replace("><","> <").split()
        m = await message.channel.fetch_message(int(id))
        if not m : return
        
        for i in emoji: 
            try:  await m.add_reaction(i.strip()) 
            except:pass
        