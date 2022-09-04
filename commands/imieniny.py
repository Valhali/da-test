from commands.base_command  import BaseCommand
import urllib.request, json, discord, requests, utils, settings
from bs4 import BeautifulSoup
from datetime import *
from dateutil.tz import *
from dateutil import tz

class Imieniny(BaseCommand):

    def __init__(self):
        description = "Dzisiejsze imieniny"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        conn = settings.conn
        c = settings.c
        id = message.guild.id

        msg=""
        
        
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
        dz = True
        msg=""
        ##########################################
        dn = datetime.now(tz.gettz('Europe/Warsaw'))
        
        if len(params)>0:
            dz=False
            p1 = message.content[len(settings.COMMAND_PREFIX)+8:].strip()
            try:
                dn=datetime.strptime(p1, '%d.%m').replace(year= dn.year)
            except:   
                try:
                    dn=datetime.strptime(p1, '%d-%m').replace(year= dn.year)
                except: 
                    try:
                        dn=datetime.strptime(p1, '%d %m').replace(year= dn.year)
                    except:     
                        try:
                            dn=datetime.strptime(p1, '%m %d').replace(year= dn.year)
                        except:
                            try:
                                dn=datetime.strptime(p1, '%m-%d').replace(year= dn.year)
                            except:   
                                try:
                                    dn=datetime.strptime(p1, '%m.%d').replace(year= dn.year)
                                except:                                                
                                    dn = datetime.now(tz.gettz('Europe/Warsaw'))
                                    dz = True
                                    if params[0]:
                                        msg2=""
                                        mi=0
                                        for j in c.execute("SELECT day, month, imieniny FROM calendar;" ):
                                            if j: 
                                                msg = json.loads(j[2])
                                                if params[0].lower() in map(lambda x: x.lower(), msg):
                                                    for i in mies:
                                                        if mies[i][1] == int(j[1]): mi = i
                                                    msg2 +="- **{}** {}\n".format(j[0],mies[mi][0])
                                                 
                                        if not msg2: msg2 = "Błąd! Nie mogą znaleźć takiego imienia."
                                        
                                        
                                        embed = discord.Embed(color=0x00ff00)
                                        embed.title = "{} obchodzi imieniny:".format(params[0].capitalize())
                                        embed.description = msg2
                                        embed.set_footer(text="Zwykle imieniny obchodzi się w dniu wypadającym jako pierwszy w kolejności po urodzinach.")
                                        await utils.send(client= client, message=message, cmd="imieniny",embed=embed)
                                                
                                        return
          
        ##########################################
        
        
        d2 = int( dn.strftime("%j"))
        m1 = int(dn.strftime("%m") )
        d = int( dn.strftime("%d"))
        wd = tyd[dn.isoweekday()]
        
        for i in mies:
            if mies[i][1] == m1: mi = i

        dzis="{} {}".format(d, mies[mi][0])

        msg=[]
        for j in c.execute("SELECT imieniny FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
            if j: msg = json.loads(j[0])
            
        if not msg:   
            await  utils.calend_update()  
            await utils.upload_sett()           
            for j in c.execute("SELECT imieniny FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
                if j: msg = json.loads(j[0])
        
        msg = ", ".join(msg)
       
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Imieniny dziś obchodzą" if dz else "Imieniny z {}".format(dzis)
        embed.description = msg
        #await message.channel.send(embed=embed)
        await utils.send(client= client, message=message, cmd="imieniny",embed=embed)
