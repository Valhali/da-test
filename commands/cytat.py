from commands.base_command  import BaseCommand
import urllib.request, json, discord, requests, utils, settings
from bs4 import BeautifulSoup
from datetime import *
from dateutil.tz import *
from dateutil import tz

class Cytat(BaseCommand):

    def __init__(self):
        description = "Cytat na dziś"
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
        dzis=""
        ##########################################
        dn = datetime.now(tz.gettz('Europe/Warsaw'))
        if len(params)>0:
            dz=False
            p1 = message.content[len(settings.COMMAND_PREFIX)+5:].strip()
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
        ##########################################
        
        
        d2 = int( dn.strftime("%j"))
        m1 = int(dn.strftime("%m") )
        d = int( dn.strftime("%d"))
        wd = tyd[dn.isoweekday()]
        
        for i in mies:
            if mies[i][1] == m1: mi = i

        dzis="{} {}".format(d, mies[mi][0])

        msg=[]
        for j in c.execute("SELECT cytat FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
            if j: msg = j[0] 
            
        if not msg:   
            await  utils.calend_update()  
            await utils.upload_sett()           
            for j in c.execute("SELECT cytat FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
                if j: msg = j[0]
        
        
        
       
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Cytat na dziś" if dz else "Cytat z {}".format(dzis)
        embed.description = msg
        #await message.channel.send(embed=embed)
        await utils.send(client= client, message=message, cmd="cytat",embed=embed)


