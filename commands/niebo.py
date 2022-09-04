from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, settings, io
from random                 import randint
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.tz import *
import utils, discord, time
from bs4 import BeautifulSoup


class Niebo(BaseCommand):

    def __init__(self):
        description = "Mapa nieba."
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        
       
        m = message.content[len(settings.COMMAND_PREFIX)+5:].strip()
        if not m :            
            await utils.send(client= client, message=message, cmd="niebo",msg="Podaj miasto i ewentualnie datę w formacie `YYYY-MM-DD HH:MM` np:\n`!niebo warszawa` lub `!niebo kraków | 2025-01-25 2:25`" )
            return
        
       
        if "|" in m:
            cmd = m.split("|")
            try:
                t1 = datetime.strptime(cmd[1].strip(), '%Y-%m-%d %H:%M')
            except:            
                await utils.send(client= client, message=message, cmd="niebo",msg="Podaj datę w formacie `YYYY-MM-DD HH:MM`" )
                return
            miasto = cmd[0].strip()
        else:
            miasto =' '.join([str(elem) for elem in params]).strip()
            t1 = datetime.now(tz.gettz('Europe/Warsaw'))
            
        h = t1.strftime("%H:%M   %d-%m-%Y")
        
        msg = ""
        if params[0] == "": 
            msg = message.author.mention +" Musisz podać miasto w komendzie!"
            await utils.send(client= client, message=message, cmd="niebo",msg=msg)
            return
        if params[0] != "":
            
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+miasto+"&appid=" + settings.WEATHER +"&units=metric&lang=pl", allow_redirects=True).content
            j = json.loads(r)
            
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=london&appid=" + settings.WEATHER +"&units=metric&lang=pl", allow_redirects=True).content
            j2 = json.loads(r)
            
        if not "coord" in j: 
            msg = "Błąd: "+j["cod"]+" Podaj prawidłowe miasto!"
            await utils.send(client= client, message=message, cmd="niebo",msg=msg)
            return    
        
        
        lat = str(j["coord"]["lat"])
        lon = str(j["coord"]["lon"])
        t = j2["timezone"] #czas gmt
        
        tj = j["timezone"] if j["timezone"]>0 else t
        
        
        n = j["name"]
        
        
        #################
        params = {
            'lat': lat,
            'lng': lon,
        }
        s = requests.Session()
        
        headers={"Host": "www.heavens-above.com",            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285",            "Referer": "https://www.heavens-above.com/SkyChart.aspx?lat={}&lng={}&loc=Unnamed&alt=0&tz=CET".format(lat, lon),            
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded"
        
        }
        s.headers.update(headers)

        
        r = s.post("https://www.heavens-above.com/SkyChart.aspx?loc=Unnamed&alt=0&tz=CET&cul=pl".format(lat, lon),
            params=params,
            data={
                'ctl00$cph1$txtYear': t1.strftime("%Y"),
                'ctl00$cph1$txtMonth': t1.strftime("%m"),
                'ctl00$cph1$txtDay': t1.strftime("%d"),
                'ctl00$cph1$txtHour': t1.strftime("%H"),
                'ctl00$cph1$txtMinute': t1.strftime("%M"),
                'ctl00$cph1$txtSize': 800,
                'utcOffset': 0,
                'ctl00$cph1$radioColours': "radioColour",
                'ctl00$cph1$chkShowLines': 1,
                'ctl00$cph1$chkShowNames': 1,
                'ctl00$cph1$chkBoundaries': "",
                'ctl00$cph1$chkEcliptic': "",
                'ctl00$ddlCulture': "pl",
                '__VIEWSTATEGENERATOR': "AF966965",
                '__VIEWSTATE': "",
                '__LASTFOCUS': "",
                '__EVENTARGUMENT': "",
                '__EVENTTARGET': "ctl00%24ddlCulture",
            }
        )
        
        
        r = r.content
        
        #################
        
        soup = BeautifulSoup(r, 'html.parser')
        results = soup.find(id='ctl00_cph1_imgSkyChart')
        
                
        
        r = s.get("https://www.heavens-above.com/"+results["src"])
        data = io.BytesIO(r.content)
        f = discord.File(data, "sky.png")
        
        if not f: return
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Mapa nieba"
        embed.description = "Miejscowość: **{}**\nData: **{}**".format( n, h ) 
        #embed.set_footer(text= "Data: {}".format( h ) )
        embed.set_image(url="attachment://sky.png")
        await utils.send(client= client, message=message, cmd="niebo",embed=embed,file= f)
        
        
        