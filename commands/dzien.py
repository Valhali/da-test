from commands.base_command  import BaseCommand
import urllib.request, json, discord, requests, utils, settings
from bs4 import BeautifulSoup
from datetime import *
from dateutil.tz import *
from dateutil import tz



class Dzien(BaseCommand):

    def __init__(self):
        description = "Dzisiejsze święta"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        conn = settings.conn
        c = settings.c
        id = message.guild.id
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
        
        ##########################################
        dn = datetime.now(tz.gettz('Europe/Warsaw'))
        if len(params)>0:
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
        ##########################################
        
        
        d2 = int( dn.strftime("%j"))
        m1 = int(dn.strftime("%m") )
        d = int( dn.strftime("%d"))
        wd = tyd[dn.isoweekday()]
        
        for i in mies:
            if mies[i][1] == m1: mi = i


        msg=[]
        calend=""
        for j in c.execute("SELECT swieto FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
            if j: calend = json.loads(j[0] )
            
        if not calend:   
            await  utils.calend_update()   
            await utils.upload_sett()                  
            for j in c.execute("SELECT swieto FROM calendar WHERE day=? AND month =? LIMIT 1;", (d,m1) ):
                if j: calend = json.loads(j [0])
        
        
        dzis="{} {}".format(d, mies[mi][0])
                
        
        msg = ", ".join(calend)
        calend = []
        for j in c.execute("SELECT swieto FROM calendar_local WHERE day=? AND month =? AND (server = ? OR server=0) ;", (d,m1, id) ):
            if j: 
                for i in j:
                    calend.append(i) 
        if calend:  msg = "{} \n\n**Święta serwerowe:**\n{}".format(msg, ", ".join(calend))

        embed = discord.Embed(color=0x00ff00)
        embed.title = "{} - {} – {}".format(wd.capitalize() ,dzis , "{} dzień roku".format(d2))
        embed.description = msg
        await utils.send(client= client, message=message, cmd="dzien",embed=embed)
