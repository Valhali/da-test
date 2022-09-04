from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, settings
from random                 import randint
from datetime import datetime, timedelta
import utils, discord, time
from bs4 import BeautifulSoup

class Satelity(BaseCommand): #satelity miejscowosc | minJasnosc | starlinki

    def __init__(self):
        description = "Info o przelotach satelit."
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        
        gc = await utils.gc(message.guild.id, "satelity", client)
        msg = ""
                           
            
        if params[0] == "": 
            msg = message.author.mention +" Musisz podać miasto w komendzie!"
            if gc: await gc.send(msg)
            else: await message.channel.send(msg)
            return
            
            
        if params[0] != "":
            params[0] =' '.join([str(elem) for elem in params])
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+params[0]+"&appid=" + settings.WEATHER +"&units=metric&lang=pl", allow_redirects=True).content
            j = json.loads(r)
            
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=london&appid=" + settings.WEATHER +"&units=metric&lang=pl", allow_redirects=True).content
            j2 = json.loads(r)
            
        if not "coord" in j: 
            msg = "Błąd: "+j["cod"]+" Podaj prawidłowe miasto!"
            if gc: await gc.send(msg)
            else: await message.channel.send(msg)
            return    
        
        
        lat = str(j["coord"]["lat"])
        lon = str(j["coord"]["lon"])
        t = j2["timezone"] #czas gmt
        
        tj = j["timezone"] if j["timezone"]>0 else t
        
        
        n = j["name"]
        
        
        
        
        
        r = requests.get("https://in-the-sky.org/satpasses.php?day=26&month=5&year=2021&mag=4&anysat=v0&group=1&s=&latitude={}&longitude={}&timezone=0&skin=1".format(lat, lon), allow_redirects=True).content
        soup = BeautifulSoup(r, 'html.parser')
        results = soup.find_all(class_='sp_target', limit=1)
        print(results)
        iss=""
               
        
        for i in results:            
            j = i.find_all("td")     
            
            print(j)
            continue
            
            t1 =  datetime.strptime(j[2].text.strip(), '%H:%M:%S')+ timedelta(seconds=-t+tj) 
            #d1 = t1.strftime("%d-%m")
            t1 = t1.strftime("%H:%M:%S")
            t2 =  datetime.strptime(j[8].text.strip(), '%H:%M:%S')+ timedelta(seconds=-t+tj) 
            t2 = t2.strftime("%H:%M:%S")
            
            iss+= "**{}**: {}mag **{}** {} {} **→** **{}** {} {}\n".format( j[0].text.strip(), j[1].text.strip(), t1, j[3].text.strip(),j[4].text.strip(), t2 , j[9].text.strip(), j[10].text.strip() ) 
            if len(iss)>1800: break
       # print(iss)
        
        return
        
        
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Przeloty satelit dla miejscowości {}".format(n) 
        embed.description = iss
        #embed.set_thumbnail(url = "https://www.heavens-above.com/orbitdisplay.aspx?icon=default&width=600&height=600&satid=25544&{}".format(time.time()))
        #if "WARIANTY" in odp : embed.add_field(name="Warianty", value="{:s}".format(odp["WARIANTY"]) )
        #if "WYMOWA" in odp : embed.add_field(name="Wymowa", value="{:s}".format(odp["WYMOWA"]) )
        #if "ODSYŁACZE" in odp : embed.add_field(name="Powiązane", value="{:s}".format(odp["ODSYŁACZE"]) )
        #if "DATA" in odp : embed.set_footer(text=odp["DATA"] )
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        #await utils.upload_sett()  