from commands.base_command  import BaseCommand
import wikipedia, discord, re, utils
from datetime import *
from dateutil.tz import *
from dateutil import tz


bot_id = "573821635677913108"
class Kalendarium(BaseCommand):

    def __init__(self):
        description = "Dzisiejsze kalendarium (uwaga na kilometrowe wiadomości :innocent: ). Dostępne kategorie: **kosmos, polska, świat, urodzeni, zmarli**"
        params = ["kategoria"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        msg=""
        m=" "
        gc = await utils.gc(message.guild.id, "kalendarium", client)
        if params:
            wikipedia.set_lang("pl")
            k = wikipedia.page("Kalendarium dzień po dniu")
            polska = k.section("Wydarzenia w Polsce")
            swiat = k.section("Wydarzenia na świecie")
            kosmos = k.section("Eksploracja kosmosu")
            if not kosmos: kosmos = k.section("Zdarzenia astronomiczne i eksploracja kosmosu")
            if not kosmos: kosmos = k.section("Eksploracja kosmosu i zdarzenia astronomiczne")
            if not kosmos: kosmos = k.section("Zdarzenia astronomiczne")
            if not kosmos: kosmos = k.section("Astronomia")
            urodzeni = k.section("Urodzili się")
            zmarli = k.section("Zmarli")
            
            dt = datetime.now(tz.gettz('Europe/Warsaw'))            
            d = dt.strftime("%d") 
            m = dt.strftime("%m") 
            
            if params[0]=="polska": 
                m="Co wydarzyło się w Polsce {}.{}:".format(d,m)
                msg=polska
            if params[0]=="swiat" or params[0]=="świat": 
                m="Co wydarzyło się na świecie {}.{}:".format(d,m)
                msg=swiat
            if params[0]=="kosmos" and kosmos != None: 
                m="Co wydarzyło się w astronomii {}.{}:".format(d,m)
                msg=kosmos
            if params[0]=="urodzeni": 
                m="Znani i urodzeni {}.{}:".format(d,m)
                msg=urodzeni
            if params[0]=="zmarli": 
                m="Znani i zmarli {}.{}:".format(d,m)
                msg=zmarli
            if kosmos == None and params[0]=="kosmos": 
                if int(bot_id) == message.author.id: return
                msg = "Tego dnia nic ciekawego nie wydarzyło się w astronomii."
                #await message.channel.send(msg)
                if gc: await gc.send(msg)
                else: await message.channel.send(msg)
                return
        if not msg : msg = message.author.mention +" Sprecyzuj swoje zapytanie dodając do komendy (po spacji) kategorie: **polska, świat, kosmos, urodzeni, zmarli** \nNp: !kalendarium polska"
        m2=""
        i=0
        mt = msg.split("\n")
        for e in mt:
            e2=e
            j = re.findall(r"^[0-9]+",e)
            if j: 
                e = e.replace(j[0], "**"+j[0]+"**")
            else: 
                e = " - "+e
            m2 += e + "\n"
            if len(m2)>1500 or e2 == mt[-1]:
                embed = discord.Embed(color=0x00ff00)
                if i==0: embed.title = m 
                embed.description = m2
                #await message.channel.send(embed=embed)
                if gc: await gc.send(embed=embed)
                else: await message.channel.send(embed=embed)
                #await message.channel.send(m2)
                m2=""
                i=1
                embed=None

