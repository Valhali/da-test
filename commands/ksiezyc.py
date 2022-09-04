from commands.base_command  import BaseCommand
import urllib.request, json, utils
import base64
import discord, settings
import re
import requests
from bs4 import BeautifulSoup
from dateutil import tz
from dateutil.tz import *
from datetime import datetime, timedelta, time

async def _moon(kierunek, proc):
    if kierunek == 0: #widocznosc maleje 
        if 2 >= proc >= 0:
            return """**Nów**
Obecna faza księżyca to nów. Oznacza to, że księżyc jest nieoświetlony. Dzieje się tak ponieważ patrząc z Ziemi Księżyc jest w koniunkcji ze Słońcem, czyli znajduje się między Ziemią, a Słońcem. Nów jest przeciwną fazą do pełni, w której cała oświetlona część Księżyca jest zwrócona w stronę Ziemi. Miesiąc synodyczny nazywany lunacją jest to okres między nowiami i średnio trwa około 29,53 dnia."""
        if 30 >= proc >=2:
            return """**Sierp (stary księżyc)**
Obecna faza Księżyca to sierp. Jest to faza Księżyca, w której oświetlona jest lewa część (w kształcie sierpa) tarczy Księżyca. Księżyc "maleje" w stronę nowiu, stąd nazwa stary księżyc."""
        if 60 >= proc >=30:
            return """**III kwadra (ostatnia)**
Obecna faza Księżyca to III (ostatnia) kwadra. Widać jeszcze całą lewą połowę tarczy Księżyca. Od nowiu Księżyc pokonał 3/4 swojej orbity."""
        if 95 >= proc >=60:
            return """**Księżyc garbaty (ubywa)**
Obecna faza Księżyca to "Księżyc Garbaty". Oświetlona część Księżyca maleje (ubywa). Widoczna jest jeszcze większa część zachodniej tarczy Księżyca, który zmierza w stronę nowiu."""
        if 95 <= proc <=100:
            return """**Pełnia Księżyca**
Obecna faza Księżyca to pełnia. Oznacza to, że cała tarcza Księżyca jest oświetlona przez Słońce. Dzieje się tak kiedy Księżyc znajduje się po przeciwnej stronie Ziemi niż Słońce. Pełnia Księżyca jest przeciwną fazą do nowiu, w którym w stronę Ziemi zwrócona jest nieoświetlona część tarczy Księżyca. Ponieważ miesiąc synodyczny średnio trwa około 29,53 dnia bywa, że w lutym nie występuje żadna pełnia."""
            
            
            
    else: 
        if 5 >= proc >0:
            return """**Nów**
Obecna faza księżyca to nów. Oznacza to, że księżyc jest nieoświetlony. Dzieje się tak ponieważ patrząc z Ziemi Księżyc jest w koniunkcji ze Słońcem, czyli znajduje się między Ziemią, a Słońcem. Nów jest przeciwną fazą do pełni, w której cała oświetlona część Księżyca jest zwrócona w stronę Ziemi. Miesiąc synodyczny nazywany lunacją jest to okres między nowiami i średnio trwa około 29,53 dnia."""
        if 25 >= proc >=5:
            return """**Sierp (młody księżyc)**
Obecna faza Księżyca to sierp. Jest to faza Księżyca, w której oświetlona jest prawa część (w kształcie sierpa) tarczy Księżyca. Księżyc "rośnie" w stronę pierwszej kwadry, stąd nazwa młody księżyc."""
        if 25 <= proc <=70 :
            return """**Pierwsza kwadra**
Obecna faza Księżyca to pierwsza kwadra. Jest to faza Księżyca, w której Ziemia, Księżyc i Słońce tworzą ze sobą kąt prosty. Oświetlona jest prawa, wschodnia część tarczy Księżyca, który zbliża się do pełni."""
        if 70 <= proc <=95:
            return """**Księżyc garbaty (przybywa)**
Obecna faza Księżyca to "Księżyc Garbaty". Jest to faza po pierwszej kwadrze, w której Księżyc zbliża się do pełni i oświetlona jest już większa część jego tarczy."""
        if 95 <= proc <=100:
            return """**Pełnia Księżyca**
Obecna faza Księżyca to pełnia. Oznacza to, że cała tarcza Księżyca jest oświetlona przez Słońce. Dzieje się tak kiedy Księżyc znajduje się po przeciwnej stronie Ziemi niż Słońce. Pełnia Księżyca jest przeciwną fazą do nowiu, w którym w stronę Ziemi zwrócona jest nieoświetlona część tarczy Księżyca. Ponieważ miesiąc synodyczny średnio trwa około 29,53 dnia bywa, że w lutym nie występuje żadna pełnia."""
    
    


class Ksiezyc(BaseCommand):

    def __init__(self):
        description = "Faza księżyca"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        conn = settings.conn
        c = settings.c
        try:
            await message.delete()
        except :
            pass
        moon = []
        y = str(datetime.now(tzutc()).year )
        now = str( datetime.now(tzutc()).strftime("%d %b %Y %H:00 UT") )
        past = datetime.now(tzutc()) + timedelta(hours=-1)
        past = str( past.strftime("%d %b %Y %H:00 UT") )
        
        for j in c.execute("SELECT time, phase, distance FROM moon WHERE time=? LIMIT 1;", (now,) ):
            if j: moon = j
        rosnie = 0
        for j in c.execute("SELECT phase FROM moon WHERE time=? LIMIT 1;", (past,) ):
            print(j,moon)
            if float(j[0]) > float(moon[1]) : rosnie = 0
            else: rosnie = 1
        if not moon: 
            r = requests.get("https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004874/mooninfo_"+y+".json", allow_redirects=True).content
            settings.MOON = json.loads(r)
        
            for i in    settings.MOON:
                date = datetime.strptime(i["time"], '%d %b %Y %H:%M UT') 
                date = str( date.strftime("%d %b %Y %H:00 UT") )
                c.execute("INSERT OR IGNORE INTO moon (time, phase, distance) VALUES (?,?,?);", (date,i['phase'],i['distance'] ))
                if now == date:
                    moon = (i['time'],i['phase'], i['distance'] )
                
            conn.commit()  
            
        for j in c.execute("SELECT time, phase, distance FROM moon WHERE time=? LIMIT 1;", (now,) ):
            if j: moon = j
        for j in c.execute("SELECT phase FROM moon WHERE time=? LIMIT 1;", (past,) ):
            if float(j[0]) > float(moon[1]) : rosnie = 0
            else: rosnie = 1
        
        if not moon: return
        nr = datetime.now(tzutc()).timetuple().tm_yday * 24 - (24 - datetime.now().hour)
        url = "https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004874/frames/730x730_1x1_30p/moon.{:04d}.jpg".format(nr);
        

        r=""
        msg = "Coś się popimpało i nie mogę zassać danych :cry: "
        
        proc = "0% widoczności"
        p = re.findall(r'\d+',proc)
        proc = proc.replace(p[0], moon[1])
        p = str( float(moon[1])/100.0 )

        if not url: url="https://kalendarz.livecity.pl/tools/moon-image.php?size=300&width="+p
        
        
        msg = await _moon(rosnie,float(moon[1]))
        
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = proc
        embed.description = msg
        embed.set_thumbnail(url=url)
        #embed.set_image(url=url)
        embed.set_footer(text = "Odległość od ziemi: {} km".format(moon[2]) )
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "ksiezyc", client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)








