from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import operator, discord

class Zlicz2(BaseCommand): # ilosc #kanał bot top

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        #if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return
        try:
            await message.delete()
        except :
            pass
        i = re.findall(r'\d+',params[1])
        ch = client.get_channel(int(i[0]) )
        b = int(params[2]) if len(params)>2 else True
        t = int(params[3]) if len(params)>3 else 10
        
        try:
            messages = await ch.history(limit=int(params[0]), oldest_first=False).flatten()
        except:
            messages=""
        top={}    
        for m in messages:
            nick=""            
            if b and m.author.bot: continue    
            nick = m.author.id
              
            if nick in top: top[nick] += 1
            else:  top[nick] = 1             
        
        s =  sorted(top.items(), key=operator.itemgetter(1),reverse=True) 
        msg = ""
        i=0
        for k,v in dict(s[0:t]).items() :
            #for k in r:
            i+=1
            k = message.guild.get_member(k)
            if not k: continue
            if isinstance(k,discord.member.Member): 
                nick = k.nick if k.nick else k.name
            else:     
                nick = k.name
            msg+="**{}**: {} - {}\n".format(i, nick,v)
            
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Najbardziej aktywni na #{} w ostatnich {} wiadomości(ach)".format(ch.name, params[0])
        embed.description = msg
        await message.channel.send(embed=embed)        
        #print(top) 
        #await utils.upload_sett()  