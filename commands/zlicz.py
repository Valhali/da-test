from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import operator, discord
from prettytable import PrettyTable

class Zlicz(BaseCommand): # ilosc #kanał bot top

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
        #print(type("FF"), type(10))
        #return
        if not params[0].isdigit(): 
            await message.channel.send("Podaj prawidłową liczbę!")
            return
            
        #isinstance(m.author,discord.member.Member)    
        i = re.findall(r'\d+',params[1])
        if not i[0].isdigit(): 
            await message.channel.send("Podaj prawidłowy kanał!")
            return
        ch = client.get_channel(int(i[0]) )
        if not ch: 
            await message.channel.send("Podaj prawidłowy kanał!")
            return
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
            if isinstance(m.author,discord.member.Member): 
                nick = m.author.nick if m.author.nick else m.author.name
            else:     
                nick = m.author.name
              
            if nick in top: top[nick] += 1
            else:  top[nick] = 1             
        
        s =  sorted(top.items(), key=operator.itemgetter(1),reverse=True) 
        msg = ""
        i=0
        
        ta = PrettyTable(['Nr', 'Nick', 'Wiadomości'])
        for k,v in dict(s[0:t]).items() :
            #for k in r:
            i+=1
            ta.add_row([i, k, v])   
            msg+="**{}**: {} - {}\n".format(i, k,v)
            
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Najbardziej aktywni na #{} w ostatnich {} wiadomości(ach)".format(ch.name, params[0])
        embed.description = "`{}`".format( ta ) 
        await utils.send(client= client, message=message, cmd="zlicz",embed=embed)  
        #print(top) 
        #await utils.upload_sett()  