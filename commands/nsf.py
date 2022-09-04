from commands.base_command  import BaseCommand
import requests
from bs4 import BeautifulSoup
import settings, discord, json, utils, re
from random                 import randint

class Nsf(BaseCommand):

    def __init__(self):
        description = "Najbliższe loty w kosmos"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        conn = settings.conn
        c = settings.c
        id = str(message.guild.id)
        msg=""   
  
        r = requests.get("https://nextspaceflight.com/launches/", allow_redirects=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find_all(class_='launch', limit=3)
        
        
        gc = await utils.gc(message.guild.id, "nsf", client)
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Najbliższe loty w kosmos"
        #embed.description = msg
        
        if results : 
        
            res = soup.find(class_='mdl-cell mdl-cell--6-col')
            img = re.findall(r"(?i)(https?://[a-z0-9\-\_\.\/]+jpg)",str(res))                       
            if img  : embed.set_thumbnail (url=img[0])

            for i in results:
                
                res = i.find(class_='mdl-card__supporting-text')
                msg = res.text.replace("  ","").replace("\n\n","\n").rstrip().strip() +" "
                res = i.find(class_='header-style') 
                msg1 = res.text.replace("  ","").replace("|","\n").rstrip().strip() +" "
                res = i.find(class_='mdl-card__title-text')
                msg2 = res.text.replace("  ","").rstrip().strip() +"\n\n"
                
                res = i.find_all(class_='mdc-button', onclick=True)
                url1 = "https://nextspaceflight.com" +  res[0]['onclick'].replace("location.href","").replace("=","").replace("'","").strip() if res else ""
                
                url2 = res[1]['onclick'].replace("window.open","").replace("(","").replace(")","").replace("'","").replace("_blank","").replace(",","").strip() if len(res)>1 else ""
                
                u = "[>szczegóły<]({})".format(url1) if url1 else ""
                u += " [>oglądaj<]({})".format(url2) if url2 else ""
                
                embed.add_field(name=msg2, value="**{}**\n{} \n{}".format(msg1, msg, u) )

            if gc: await gc.send(embed=embed)
            else: await message.channel.send(embed=embed)


