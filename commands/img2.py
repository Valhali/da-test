from commands.base_command  import BaseCommand
import requests, urllib, random, time
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord
import TenGiphPy

class Img(BaseCommand): 

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
            
        API_KEY = settings.API_KEY
        SEARCH_ENGINE_ID = settings.SEARCH_ENGINE_ID
        
        
        link =[]
        cmd = message.content[len(settings.COMMAND_PREFIX)+3:].strip()
        if not cmd : return
        #for i in range(0,3):
        try:          
            #time.sleep(1)
            #request = urllib.request.Request( 
             #   'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +
             #   SEARCH_ENGINE_ID + '&q=' + cmd + '&searchType=image' )  #&start='+str(i*10)
            #time.sleep(10)
           # with urllib.request.urlopen(request) as f:       
            #    print(f)
            #    data = f.read().decode('utf-8')     
              
            print("1")
            r = requests.get('https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +                SEARCH_ENGINE_ID + '&q=' + cmd + '&searchType=image',headers={'referer': 'https://heroku.com'}, allow_redirects=True)
            data = r.content.decode('utf-8')   
              
            print("2")
                #time.sleep(int(f.headers["Retry-After"]))
                
            data = json.loads(data)
            print("3", data)
            
            for j in data['items']:
                link.append(j['link'])
            print("4", link)
        except :
            print("Nie działa")
            pass
        
        print('https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +                SEARCH_ENGINE_ID + '&q=' + cmd + '&searchType=image')
        
        print(link)
        if not link: return
        url = random.choice(link)
        
        
        
        embed = discord.Embed(color=0x00ffFF)
        #embed.title = cmd
        #embed.description = i[1]
        if url: 
            embed.set_image( url=url)
                        
        await message.channel.send(embed=embed)
        