from commands.base_command  import BaseCommand
import urllib.request, json, utils
import base64
import discord
import re
import requests
from bs4 import BeautifulSoup

from requests_html import AsyncHTMLSession
from requests_html import HTMLSession
from pprint import pprint

class Ksiezyc2(BaseCommand):

    def __init__(self):
        description = "Faza księżyca"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
            
            
##############################################
        #nest_asyncio.apply()
        session = AsyncHTMLSession()
        try:
            r = await session.get("https://svs.gsfc.nasa.gov/Gallery/moonphase.html")
            await r.html.arender(timeout=60)
        except Exception as e:
            print("Errorrrrr: %s" % e)
        
        url=""
        soup = BeautifulSoup(r.html.html, 'html.parser')
        results = soup.find("img", id='moon_image')
        if results: 
            url = results["src"]
            if results["src"][0:7] != "http://" and results["src"][0:8] != "https://" :  
                url = "https://svs.gsfc.nasa.gov" + results["src"]
     
            
        proc=""
        r = requests.get("http://kalendarz.livecity.pl/faza-ksiezyca", allow_redirects=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find("p", class_='lead')
        if results : msg = results.text.strip()
        msg = msg.replace("noiwu", "nowiu")
        
        results = soup.find( class_='col-sm-3 text-center').find("p", class_='small text-muted')              
        if results : proc = results.text.strip()
        
        p = re.findall(r'\d+',proc)
        p = str( int(p[0])/100.0 )

        if not url: url="https://kalendarz.livecity.pl/tools/moon-image.php?size=300&width="+p

        embed = discord.Embed(color=0x00ff00)
        embed.title = proc
        embed.description = msg
        embed.set_thumbnail(url=url)
        #embed.set_image(url=url)
        await message.channel.send(embed=embed)








