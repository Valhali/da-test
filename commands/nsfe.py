from commands.base_command  import BaseCommand
import requests
from bs4 import BeautifulSoup
import settings, discord, json, utils, re
from random                 import randint

class Nsfe(BaseCommand):

    def __init__(self):
        description = "Podbój kosmosu - najbliższe wydarzenia"
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
  
        r = requests.get("https://nextspaceflight.com/events/", allow_redirects=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find_all(class_='mdl-grid mdl-grid--no-spacing', limit=1)
        results = results[0].find_all(class_='mdl-grid', limit=3)

        
        gc = await utils.gc(message.guild.id, "nsf", client)
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Podbój kosmosu - najbliższe wydarzenia"
        #embed.description = msg
        
        if results : 
        
            res = soup.find(class_='mdl-grid')
            img = re.findall(r"(?i)(https?://[a-z0-9\-\_\.\/]+[jpg|jpeg|png])",str(res))
            print(img)                       
            if img  : embed.set_thumbnail (url=img[0])

            
            for i in results:
                res = i.find(class_='mdl-card__supporting-text')
                msg = res.text.replace("  ","").replace("\n\n","\n").rstrip().strip() +" "
                res = i.find(class_='header-style') 
                msg1 = res.text.replace("  ","").replace("|","\n").rstrip().strip() +" "
                res = i.find(class_='mdl-card__supporting-text b')
                msg2 = res.text.replace("\n"," ").replace("  ","").rstrip().strip() 
                
                res = i.find_all(class_='mdl-card__actions mdl-card--border')

                res = res[0].find_all(class_='mdc-button', onclick=True)
                u = ""
                for k in res:                    
                    s = k.text.strip().rstrip()
                    url = k['onclick'].replace("window.open","").replace("(","").replace(")","").replace("'","").replace("_blank","").replace(",","").strip() if len(res)>0 else ""
                
                    if s == "Info": u += " [>szczegóły<]({})".format(url) if url else ""
                    if s == "Watch": u += " [>oglądaj<]({})".format(url) if url else ""
                
                
                embed.add_field(name=msg1, value="**{}**\n{} \n{}".format(msg2, msg, u) )
                
            if gc: await gc.send(embed=embed)
            else: await message.channel.send(embed=embed)


