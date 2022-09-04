from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, settings, io
import utils, discord, time
from prettytable import PrettyTable


class Cmdstats(BaseCommand):

    def __init__(self):
        description = ""
        params = [""]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072" and not client.user.id == message.author.id:
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return
    
    
        try:
            await message.delete()
        except :
            pass
        
        stats={}
        stats2={}
        conn = settings.conn
        c = settings.c
        for i in c.execute("SELECT conf FROM config WHERE id=? AND serwer=?;", ("stats",0) ): #global
            if i : 
                stats = json.loads(i[0])
                break
            
            
        for j in c.execute("SELECT conf FROM config WHERE id=? AND serwer=?;", ("stats",message.guild.id) ): #local
            if j : 
                stats2 = json.loads(j[0])
                break
            
            
            
        ta = PrettyTable(['Komenda', 'Lokalnie', 'Globalnie'])
        key = sorted(dict(stats).items())
            
        cmds =["sql","pods"]    
        for k,v in dict(key).items() :
            ln = stats2[k] if k in stats2 else 0          
            if not k in cmds: ta.add_row([k, ln, v])   
            
        key = sorted(dict(stats2).items())
            
        for k,v in dict(key).items() :
            if not k in stats:     ta.add_row([k, stats2[k], "-"])   
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Statystyka użycia komend"
        embed.description = "`{}`".format( ta ) 
        embed.set_footer(text= "Dane zbierane od 27-06-2021" )
        await utils.send(client= client, message=message, cmd="cmdstats",embed=embed)
        
        
        