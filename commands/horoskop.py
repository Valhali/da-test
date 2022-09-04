from commands.base_command  import BaseCommand
import requests
from bs4 import BeautifulSoup
import settings, discord, json, utils
from random                 import randint

class Horoskop(BaseCommand):

    def __init__(self):
        description = "Horoskop na dziś"
        params = ["znak zodiaku"]
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
        if params:        
        ####################################
            cnf = {}
            params[0]= params[0].lower()
            cmd = message.content[len(settings.COMMAND_PREFIX)+8:].strip().lower()
            odp=[]
            for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=?;", (id,"horoskop_"+cmd) ):
                if j: cnf=json.loads(j[0])
                
            for i in cnf:
                if i: odp.append(cnf[i])
            if odp: msg = odp[randint(1, len(odp)-1)]
        ####################################
    
            if params[0]=="bliźnięta" or params[0]=="bliźnieta" or params[0]=="bliznięta" : params[0]="bliznieta"
            if params[0]=="koziorożec" : params[0]="koziorozec"
            if params[0] !="" and not odp:
                r = requests.get("https://horoskopy.gazeta.pl/horoskop/"+params[0]+"/dzienny/", allow_redirects=True)
                soup = BeautifulSoup(r.content, 'html.parser')
                results = soup.find(class_='lead')
                if results : msg = results.text.strip()

        gc = await utils.gc(message.guild.id, "horoskop", client)

        if not msg : 
            msg = message.author.mention +" Sprecyzuj swoje zapytanie dodając do komendy znak. Np: "+settings.COMMAND_PREFIX+"horoskop waga"
            #await message.channel.send(msg)
            if gc: await gc.send(msg)
            else: await message.channel.send(msg)
            return
            
        #znak = params[0]
        znak = cmd
        if znak=="bliznieta": znak = "bliźnięta"
        if znak=="koziorozec": znak = "koziorożec"
        
        
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Horoskop - " +znak.capitalize()
        embed.description = msg
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)


