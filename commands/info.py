from commands.base_command  import BaseCommand
import urllib.request, json
import base64
import discord
import re
import requests, io, discord, utils, time, settings
from datetime import datetime, timedelta
from dateutil.tz import *
from random                 import randint
#from tabulate import tabulate




class Rinfo(BaseCommand):

    def __init__(self):
        description = "Info o użytkowniku, serwerze, kanale itp."
        params = ["ID/@nick/#kanał/serwer/boost"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        
        embed = discord.Embed(color=0x0066ff)
        m = """Prawidłowe użycie komendy:
        
        `!rinfo ???` - gdzie `???` to @użytkownik, #kanał, jakieś discordowe ID lub słowa "serwer", "boost"
        
        **KOMENDA W BUDOWIE - MOŻE NIE DZIAŁAĆ!**
        
        Więcej możliwości w przyszłości.
        """             
        embed.description = m
        
        if not params[0]:
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        msg = message.content[7:].strip()
        id = re.findall(r'\d+', params[0])
        
        g =None
        u =None
        ch =None
        rol =None
        m2 = None
        
        if id and len(id[0])==18:
            try:
                g = client.get_guild(int(id[0]) )                          
                ch = client.get_channel(int(id[0]) )                          
                u =  message.guild.get_member(int(id[0]) )
                rol =  message.guild.get_role(int(id[0]) )
                if not g and not ch and not u and not rol:
                    for channel in message.guild.text_channels:
                        try:
                            m2 = await channel.fetch_message(int(id[0]) )
                            if not None == m2: break
                        except:pass
            except: pass
        else: #szukaj po nazwie
            u = message.guild.get_member_named(msg)
            rol = discord.utils.get(message.guild.roles,name=msg)
            if not u and not rol:
                for channel in message.guild.channels:                
                    if channel.name.lower() == msg.lower():
                        ch = channel
                        break
       
       
        
        if g or params[0].lower() =="serwer" or params[0].lower()=="server" or params[0].lower()=="srv":
            g = g if g else message.guild
            banner = message.guild.banner_url_as(format='jpg', size=2048)
            if not banner: banner = message.guild.discovery_splash_url_as(format='jpg', size=2048)
            
            embed.set_image(url= banner)
            embed.set_thumbnail(url= message.guild.icon_url_as(static_format='jpg', size=1024) )
            
            embed.title = "Info o serwerze {}".format(message.guild.name)
            d = """Data powstania: **{} UTC**
            Właściciel: **{}**
            Region: **{}**
            Użytkowników: **{}**
            
            Boostujących serwer: **{}**
            Poziom ulepszenia: **{}**
            Kanały tekstowe: **{}**
            Kanały głosowe: **{}**
            Ilość ról: **{}**
            Ilość emoji: **{} / {}**
            Ilość emoji animowanych: **{} / {}**
            
            """
            anim = 0
            emo = 0
            for i in g.emojis:
                if i.animated: anim = anim+1
                else: emo = emo+1
            
            d = d.format( g.created_at.strftime("%d-%m-%Y %H:%M"), 
                            g.owner.display_name, g.region, 
                            g.member_count, g.premium_subscription_count,
                            g.premium_tier, len(g.text_channels), len(g.voice_channels),
                            len(g.roles), emo, g.emoji_limit, anim, g.emoji_limit, 
                                                      )
            if g.rules_channel:     d = d + "Regulamin: {}\n".format(g.rules_channel.mention)
                
                
            if g.description:       d = d + "Opis serwera: {}".format(g.description)
            
            embed.description =  d
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
        
        if params[0].lower() =="boost":
            embed.title = "Osoby boostujące serwer!"
            m = ""
            for i in message.guild.premium_subscribers:
                m = m + "**{}**\n".format(i.mention)
                
                
            if m: m = m+"\n\nChwała Wam za to! :thumbsup_tone1: "
            if not m: m ="Brak :frowning: "
            embed.description =  m
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
        
        
        
        
        
        if u :        
            embed = discord.Embed(color= u.color )                
            embed.set_thumbnail(url= u.avatar_url_as(format='jpg', size=2048))
            
            embed.title = "Info o użytkowniku"
            d = """Użytkownik: **{}#{}**
            Nazwa wyświetlana: **{}**
            Zarejestrowany: **{} UTC**
            Na serwerze od: **{} UTC**
            Bot: **{}**
            
            Najwyższa rola: {}
            Pozostałe role: {}
            
            """
            bot = "Tak" if u.bot else "Nie"
            
            prem = u.premium_since
            if prem: d = d+"Boost serwera od: "+prem.strftime("%d-%m-%Y %H:%M UTC")
            
            for a in u.activities:
                print(a)
            #print(u.guild_permissions)
            
            r=[]
            r2=""
            for i in u.roles:
                if not i == u.top_role and not i.name =="@everyone": 
                    r.append(i.mention)                    
                    #d2 = "{}  ".format(d2, i.mention)
                    #if len(d) + len(d2)>1970: break
                    
            r3="" 
            j=0
            if r :
                for i in r:
                    if len(d) + len(r2)>1970:
                        j=j+1
                        r3 = "[+{} inna/e]".format(j)
                    else: r2 = "{} {}".format(r2, i)
                if j>0: r2 = "{} {}".format(r2, r3)    
            else: r2 = "**Brak**"
            
            d = d.format(  u.name, u.discriminator, 
                            u.display_name, u.created_at.strftime("%d-%m-%Y %H:%M"), u.joined_at.strftime("%d-%m-%Y %H:%M"),
                            bot, u.top_role.mention , r2       )
            
            
            
            embed.description =  d
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
        
         
        
        if ch :        
           
            embed.title = "Info o kanale"
            d = """Nazwa: {}
            Data powstania: **{} UTC**
            Kategoria: **{}**
            Typ: **{}**
            
            """    
            typ ="?"
            t = str(ch.type)
            if t =="text": typ ="Tekstowy"           
            if t =="voice": typ ="Głosowy"           
            if t =="category": typ ="Kategoria"           
            if t =="private": typ ="Prywatny"           
            if t =="group": typ ="Grupowy"           
            if t =="news": typ ="Ogłoszenia"           
            if t =="store": typ ="Sklep"           
            if t =="stage_voice": typ ="Scena"   
                   
            
            d = d.format(  ch.mention, ch.created_at.strftime("%d-%m-%Y %H:%M"), ch.category.mention , typ  )
            
            
            
            embed.description =  d
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
        
        
        if rol :        
            embed = discord.Embed(color= rol.color )  
            embed.title = "Info o roli"
            d = """Nazwa: {}
            Data powstania: **{} UTC**
            Pingowalna: **{}**
            Dla botów: **{}**
            Dla boosterów: **{}**
            Wyświetl osobno: **{}**
            """     
                   
            ping = "Tak" if rol.mentionable else "Nie"
            b = "Tak" if rol.is_bot_managed() else "Nie"
            bo = "Tak" if rol.is_premium_subscriber() else "Nie"
            h = "Tak" if rol.hoist else "Nie"
            
            d = d.format(  rol.mention, rol.created_at.strftime("%d-%m-%Y %H:%M"),
                            ping, b, bo, h )                    
                            
            embed.description =  d
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
     
        
        if m2 :        
            embed.title = "Info o wiadomości"
            d = """[ Link do wiadomości ]({})
            Kanał: {}
            Data wiadomości: **{} UTC**
            """                   
            
            d = d.format(  m2.jump_url, m2.channel.mention, m2.created_at.strftime("%d-%m-%Y %H:%M"),)                    
                            
            embed.description =  d
            await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
            return
        
        
        
     
        
        

        
        
        
        embed.title = ""
        embed.description = m
        
        await utils.send(client= client, message=message, cmd="rinfo",embed=embed )
        return
        
       
       
       
       
       ##################################################################
        await utils.send(client= client, message=message, cmd="nasa",embed=embed )








