from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import operator, discord

class Srv(BaseCommand): # 

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        #if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            #await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            #return
        try:
            await message.delete()
        except :
            pass




        srv="Nazwa (ludziki + boty)\n\n"
        servers = client.guilds
        for s in servers:
            srv += "→ "+ s.name +" ("+ str(s.member_count) +")\n"
            
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Serwery z Rudą"
        embed.description = srv
        await message.channel.send(embed=embed)        
        #print(top) 
        #await utils.upload_sett()  