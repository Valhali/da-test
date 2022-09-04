from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json, discord, utils
#from PIL import Image, ImageDraw, ImageFont
import settings
from datetime import datetime

class Pogoda(BaseCommand):

    def __init__(self):
        description = "Pogoda"
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
            
        msg = ""
        if params[0] == "": 
            msg = message.author.mention +" Musisz podać miasto w komendzie!"
            await utils.send(client= client, message=message, cmd="pogoda",msg=msg)
            return
        if params[0] != "":
            params[0] =' '.join([str(elem) for elem in params])
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+params[0]+"&appid=" + settings.WEATHER +"&units=metric&lang=pl", allow_redirects=True).content
            j = json.loads(r)
            
            if not "coord" in j: 
                msg = "Błąd: "+j["cod"]+" Podaj prawidłowe miasto!"
                await utils.send(client= client, message=message, cmd="pogoda",msg=msg)
                return
                
            if "coord" in j :
                t = datetime.fromtimestamp(j["sys"]["sunrise"] +j["timezone"])
                t2 = datetime.fromtimestamp(j["sys"]["sunset"] +j["timezone"])
                lat = str(j["coord"]["lat"])
                lon = str(j["coord"]["lon"])
                r2 = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid=" + settings.WEATHER +"&lang=pl&units=metric", allow_redirects=True).content
                j2 = json.loads(r2)
                msg = j['weather'][0]['description'].capitalize()  +"\n"
                msg += "Temp: "+str(j['main']['temp'])+"°C, odczuwalna: "+str(j['main']['feels_like'])+"°C\n"
                msg += "Wilgotność: "+str(j['main']['humidity']) +"%\n"
                msg += "Ciśnienie: "+str(j['main']['pressure']) +"hPa\n"
                msg += "Wiatr: {:.2f}".format(j['wind']['speed']*3.6)+"km/h\n"
                msg += "Wschód słońca: "+str(t.hour)+":{:02d}".format(t.minute)+ ", zachód: "+str(t2.hour)+":{:02d}".format(t2.minute)
        #await message.channel.send(msg)
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = j["name"] +" ("+j["sys"]["country"]+")"
        embed.description = msg 
        embed.set_thumbnail(url="http://openweathermap.org/img/wn/{:s}@4x.png".format(j['weather'][0]["icon"]) )
        #await message.channel.send(embed=embed)
        await utils.send(client= client, message=message, cmd="pogoda",embed=embed)
