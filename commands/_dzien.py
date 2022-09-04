from commands.base_command  import BaseCommand
import urllib.request, json, discord, requests, utils
from bs4 import BeautifulSoup
from datetime import *
from dateutil.tz import *
from dateutil import tz

class _Dzien(BaseCommand):

    def __init__(self):
        description = "Dzisiejsze święta"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        id = str(message.guild.id)
        mies={"Styczeń": ["stycznia",1],
        "Luty": ["lutego",2],
        "Marzec":["marca",3],
        "Kwiecień":["kwietnia",4],
        "Maj":["maja",5],
        "Czerwiec":["czerwca",6],
        "Lipiec":["lipca",7],
        "Sierpień":["sierpnia",8],
        "Wrzesień":["września",9],
        "Październik":["października",10],
        "Listopad":["listopada",11],
        "Grudzień":["grudnia",12]}
        
        tyd = ["","poniedziałek","wtorek", "środa", "czwartek","piątek", "sobota","niedziela"]
        dn =        datetime.now(tz.gettz('Europe/Warsaw'))
        d2 = int( dn.strftime("%j"))
        m1 = int(dn.strftime("%m") )
        d = int( dn.strftime("%d"))
        wd = tyd[dn.isoweekday()]
        
        for i in mies:
            if mies[i][1] == m1: mi = i


        msg=[]
        dzis="{} {}".format(d, mies[mi][0])
        
        r = requests.get("http://www.kalbi.pl/{}-{}".format(d,mies[mi][0]), allow_redirects=True)
        try:
            soup = BeautifulSoup(r.content, 'html.parser')
            results = soup.find( class_='calCard-ententa').findAll( "a")
            #d = soup.find( class_='calCard-day').text.strip()
            #d2 = soup.find( class_='calCard-dayyear').text.strip()
            #mi = soup.find( class_='calCard-month').text.strip()
            m2 = soup.find( class_='calCard-fete')
            m2 = m2.findAll( "a") if m2 else ""
            #wd = soup.find( class_='calCard-day-week').text.strip()
            if m2:
                for m in m2:
                    if m : msg.append(m.text.strip())
            for m in results:
                if m : msg.append(m.text.strip())
        except:pass    
        soup=None
        
        r = requests.get("http://nonsa.pl/wiki/Kalendarz_%C5%9Bwi%C4%85t_nietypowych", allow_redirects=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find("a", title=dzis).parent.text
        
        results = results.replace(dzis+" – ","").split(", ")
        for m in results:
            if m.lower() and not m.strip().lower() in map(str.lower ,msg): msg.append(m.strip())
        
        
        
        data={}
        with urllib.request.urlopen("http://do-liczyk.sourceforge.io/bocinka/?da={}&mo={}".format(d, mies[mi][1] )) as url:        
            data = json.loads(url.read().decode())
        if data:    
            for m in data["calendar"]["global"]:
                if m.lower() and not m.strip().lower() in map(str.lower ,msg): msg.append(m.strip())
                     
            for m in data["calendar"]["server"]:
                if m and m == id:
                    for a in data["calendar"]["server"][m]:           
                        if a.lower() and not a.strip().lower() in map(str.lower ,msg): msg.append(m.strip()) 
                
        
        msg = ", ".join(msg)

        embed = discord.Embed(color=0x00ff00)
        embed.title = "{}, {} – {}".format(wd.capitalize() ,dzis , "{} dzień roku".format(d2))
        embed.description = msg
        #await message.channel.send(embed=embed)
        await utils.send(client= client, message=message, cmd="dzien",embed=embed)
