from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import operator, discord
from datetime import *
from dateutil.tz import *
from dateutil import tz
#from tabulate import tabulate
from prettytable import PrettyTable

class Pods(BaseCommand): #kanał

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
            
        i = re.findall(r'\d+',params[0])
        if not i[0].isdigit(): 
            await message.channel.send("Podaj prawidłowy kanał!")
            return
        ch = client.get_channel(int(i[0]) )
        if not ch: 
            await message.channel.send("Podaj prawidłowy kanał!")
            return
        
        try:        
            t1 = (datetime.now(tz.gettz('Europe/Warsaw'))+ timedelta(hours=-24)).strftime("%d-%m-%Y") 
            t1= datetime.strptime(t1,"%d-%m-%Y")
            t2 = (datetime.now(tz.gettz('Europe/Warsaw'))+ timedelta(hours=-0)).strftime("%d-%m-%Y") 
            t2 = datetime.strptime(t2,"%d-%m-%Y")
            
            print(t1, t2)
            messages = await ch.history(limit=1000000,  after=t1, before=t2).flatten()
        except:
            print("zzzz")
            messages=""
        top={}    
        lm = len(messages)
        if lm ==0: return
        print("Wiadomości: ", lm)
        for m in messages:
            nick=""            
            if isinstance(m.author,discord.member.Member): 
                nick = m.author.nick if m.author.nick else m.author.name
            else:     
                nick = m.author.name
            if len(params)>1: print ( nick)  
            if nick in top: top[nick] += 1
            else:  top[nick] = 1             
        
        s =  sorted(top.items(), key=operator.itemgetter(1),reverse=True) 
        msg = ""
        i=0
        t=20
        #for k,v in dict(s[0:t]).items() :
        #    i+=1
        #    msg+="**{}**: {} - **{}**   *{:.0f}%*\n".format(i, k,v,v/lm*100)
        ############################    
        #tab = []
        ta = PrettyTable(['Nr', 'Nick', 'Wiad.', 'Procent'])
        for k,v in dict(s[0:t]).items() :
            i+=1
            #tab.append(["{}".format(i),k,"{}".format(v),"{:.1f}".format(v/lm*100)])
            ta.add_row(["{}".format(i),k,"{}".format(v),"{:.1f}".format(v/lm*100)])   
        #tabu = tabulate(tab, headers=[ 'Nr', 'Nick', 'Wiad.', 'Procent'])
        #msg = "`{}`".format( tabu )
        msg = "`{}`".format( ta )
        #print(tabu)        
        #print(ta)        
        ############################   
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Posumowanie wczorajszej aktywności na #{}".format(ch.name)
        embed.description = msg
        embed.set_footer(text = "Wszystkich wiadomości: {}".format(lm))
        await message.channel.send(embed=embed)        
        #print(top) 
        #await utils.upload_sett()  