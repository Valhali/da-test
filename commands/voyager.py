from cgi import print_directory
from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import urllib.request, json, discord, utils
import requests
from datetime import *
from dateutil.relativedelta import relativedelta
from dateutil import tz
from dateutil.tz import *
import time 
from bs4 import BeautifulSoup

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Voyager(BaseCommand):

    def __init__(self):
        description = "Info o odległości obu sond Voyager"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        now = datetime.now()
        now2 = time.time()
        start = []    
        start.append (datetime.strptime("05 09 1977 12:56:00 UTC", '%d %m %Y %H:%M:%S UTC')  ) #1 
        start.append (datetime.strptime("20 08 1977 14:29:00 UTC", '%d %m %Y %H:%M:%S UTC')  ) #2 
        
        t1 = datetime.now(tz.gettz('Europe/Warsaw'))
        diff = []
        diff.append(relativedelta(now, start[0]))
        diff.append(relativedelta(now, start[1]))
        

        diff[0] = "{0.years}l, {0.months}m, {0.days}d {0.hours}:{0.minutes}:{0.seconds}".format(diff[0])  
        diff[1] = "{0.years}l, {0.months}m, {0.days}d {0.hours}:{0.minutes}:{0.seconds}".format(diff[1])  
            
		#################
        lat = 52
        lon = 21
        params = {
            'lat': lat,
            'lng': lon,
        }
        s = requests.Session()
        
        headers={"Host": "www.heavens-above.com",            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285",            "Referer": "https://www.heavens-above.com/SolarEscape.aspx?lat={}&lng={}&loc=Unnamed&alt=0&tz=CET".format(lat, lon),            
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded"
        
        }
        s.headers.update(headers)

        
        r = s.post("https://www.heavens-above.com/SolarEscape.aspx?lat={}&lng={}&loc=Unnamed&alt=0&tz=CET&cul=pl".format(lat, lon),
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
        # odległość = odległość_początkowa + promień * sin ( czas * 2π / długość_roku + faza ) + prędkość * czas
        #################
        
        soup = BeautifulSoup(r, 'html.parser')
        img1 ="https://heavens-above.com/" 
        img1 += soup.find(id='ctl00_cph1_imgFromPole')["src"]  
        img2 ="https://heavens-above.com/" 
        img2 += soup.find(id='ctl00_cph1_imgFromSide')["src"  ]

        results = soup.find(class_='standardTable').find("tbody")        
        k=[] 
        for i in results:
            k.append(i)        
        au = 149597871

        au1z = float(k[7].find_all("td")[4].get_text().replace(',', '.'))
        km1z = au1z * au
        au1s = float(k[0].find_all("td")[4].get_text().replace(',', '.'))
        km1s = au1s * au
        lh1 = float(k[8].find_all("td")[4].get_text().replace(',', '.'))
        lh1 = int(lh1)+ (lh1-int(lh1))*6000/3600
        
        
        au2z = float(k[7].find_all("td")[3].get_text().replace(',', '.'))
        km2z = au2z * au
        au2s = float(k[0].find_all("td")[3].get_text().replace(',', '.'))
        km2s = au2s * au
        lh2 = float(k[8].find_all("td")[3].get_text().replace(',', '.'))
        lh2 = int(lh2)+ (lh2-int(lh2))*6000/3600

        
        embed = discord.Embed(color=0x00ff00)
        msg = ""
        msg += "Start: 05-09-1977 12:56 UTC\n"
        msg += "Prędkość: {:.2f} km/s\n".format(float(k[1].find_all("td")[4].get_text().replace(',', '.')) )
        msg += "Odległość od ziemi: {:,.0f} km ({:,.3f} AU)\n".format(km1z,au1z).replace(',', ' ')
        msg += "Odległość od słońca: {:,.0f} km ({:,.3f} AU)\n".format(km1s,au1s).replace(',', ' ')
        msg += "Pokonanie takiej odległości zajęło "+diff[0]+" a z prędkością światła wystarczyłoby {:s}.\nTak daleko a tak blisko...".format(time.strftime('%H:%M:%S', time.gmtime(lh1*3600)) )

        
        
        embed.add_field(name="Voyager 1", value=msg )
        
        msg = ""
        msg += "Start: 20-08-1977 14:29 UTC\n"
        msg += "Prędkość: {:.2f} km/s\n".format( float(k[1].find_all("td")[3].get_text().replace(',', '.')) )
        msg += "Odległość od ziemi: {:,.0f} km ({:,.3f} AU)\n".format(km2z, au2z).replace(',', ' ')
        msg += "Odległość od słońca: {:,.0f} km ({:,.3f} AU)\n".format(km2s,au2s).replace(',', ' ')
        msg += "Pokonanie takiej odległości zajęło "+diff[1]+" a z prędkością światła wystarczyłoby {:s}.".format(time.strftime('%H:%M:%S', time.gmtime(lh2*3600)))

        embed.add_field(name="Voyager 2", value=msg, inline=False )

        f = await utils.dimg(img1,"1.png")
        f2 = await utils.dimg(img2,"2.png")
        embed.set_image(url="attachment://1.png")
        embed.set_thumbnail(url="attachment://2.png")
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "voyager", client)
        if gc: await gc.send(embed=embed,files= [ f, f2])
        else: await message.channel.send(embed=embed,files= [f, f2] )

        #await message.channel.send(msg)
