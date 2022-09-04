from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord
import TenGiphPy

class Gif(BaseCommand): #tytul | opis | img |thumb

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Komenda testowa - musisz być modkiem by z niej korzystać")
            return

        try:
            await message.delete()
        except :
            pass         
            
        
        cmd = message.content[len(settings.COMMAND_PREFIX)+3:].strip()
        if not cmd : return
        
        t = TenGiphPy.Tenor(token='77LXLCAA979K')
        gif = t.random(cmd)       
        
        embed = discord.Embed(color=0x00ffFF)
        #embed.title = cmd
        #embed.description = i[1]
        if gif: 
            embed.set_image( url=gif)
                        
        await message.channel.send(embed=embed)
        