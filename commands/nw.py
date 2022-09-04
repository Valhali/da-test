from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, settings
from random                 import randint
from datetime import datetime
import utils 
import wikipedia, discord
from bs4 import BeautifulSoup

class Nw(BaseCommand):

    def __init__(self):
        description = "Losowe nowe wyrazy, które pojawiły się w internecie w ostatnich latach."
        params = ["nic lub początek słowa"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        url0="https://nowewyrazy.uw.edu.pl{}"
        gc = await utils.gc(message.guild.id, "nw", client)
        if params:
            msg = ' '.join([str(elem) for elem in params])            
            if not settings.SLOWA:
                r = requests.get("https://nowewyrazy.uw.edu.pl/lista-hasel/wszystkie/wg-tytulu.html#A", allow_redirects=True)
                soup = BeautifulSoup(r.content, 'html.parser')
                results = soup.find_all(class_=['entry-type-0','entry-type-1'])
                
                slownik = []
                for i in results:
                    slownik.append({i.text.strip() : i.a['href']})
                settings.SLOWA = slownik
            else: slownik  = settings.SLOWA
            slownik2 =[]  
            for i in slownik:
                if list(i.keys())[0].startswith(msg) : slownik2.append(i) 
            slownik = ''
            
            if not slownik2:      
                m = "Coś nie mogę znaleźć słowa z takim początkiem"
                if gc: await gc.send(m)
                else: await message.channel.send(m)
                return
            
        else: return
        r = randint(0, len(slownik2)-1)
        slowo = list(slownik2[r].keys())[0]
        url = url0.format(slownik2[r][slowo])
        odp = {}
        for k in range(0,3):
            req = requests.get(url, allow_redirects=True)
            soup2 = BeautifulSoup(req.content, 'html.parser')
            res = soup2.find(id='entry')
            tr = res.find_all("tr")
            if len(tr)<=1:
                res = tr[0].find(class_='referrer').find("a")
                url = url0.format(res["href"]).replace("../","/").replace("///","/")
                print("→ przekierowanie!!!")
                continue
                
            for i in tr:
                if not i: continue
                j = i.find_all("td")
                odp[j[0].text.strip()] = j[1].text.strip()

            break
        
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = odp["HASŁO"]
        embed.description = odp["DEFINICJA"]
        if "WARIANTY" in odp : embed.add_field(name="Warianty", value="{:s}".format(odp["WARIANTY"]) )
        if "WYMOWA" in odp : embed.add_field(name="Wymowa", value="{:s}".format(odp["WYMOWA"]) )
        if "ODSYŁACZE" in odp : embed.add_field(name="Powiązane", value="{:s}".format(odp["ODSYŁACZE"]) )
        if "DATA" in odp : embed.set_footer(text=odp["DATA"] )
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        #await utils.upload_sett()  