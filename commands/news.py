from commands.base_command  import BaseCommand
import settings
import re, os, settings
import utils, discord
from discord.ext import commands

class News(BaseCommand): 

    def __init__(self):
        description = "Wysyłanie wiadomości przez botkowy newsletter."
        #description = ""
        params = ["kanał", "wiadomość"]
        super().__init__(description, params)

    async def handle(self, params, message, client):        
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072" and not "newsman" in [y.name.lower() for y in message.author.roles]:
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return
        try:
            await message.delete()
        except :
            pass
        
        conn = settings.conn
        c = settings.c
        
        id = message.guild.id
        
        m = re.search(params[0], message.content)
        opis = message.content[m.end():].strip()
        
        #opis = " ".join([str(elem) for elem in params[1:]])
        nazwa = params[0].lower()
        
        n = False    
        for j in c.execute("SELECT id FROM config WHERE id=? AND serwer=?;",("news_"+nazwa, id ) ):
            if j: n = True     
            
        if not n: # 
            await utils.send(client= client, message=message, cmd="news",msg="Nie ma kanału o takiej nazwie lub próbujesz wysłać wiadomość z innego serwera niż był zarejestrowany kanał!")
            return
            
            
        embed = discord.Embed(color=0xFF0066)
        embed.title = nazwa.capitalize()
        embed.description = opis
        embed.set_footer(text = message.author.display_name )
        
        i=0
        c.execute("SELECT chan, srv FROM newssub WHERE news=?;",(nazwa, ) )
        o = c.fetchall()
        for j in o:
            print(j)
            if j: 
                try:
                    channel = client.get_channel(int(j[0]))
                    await channel.send( embed=embed  )
                    i=i+1
                    channel=''
                except: 
                    print("NEWS: błąd")

                    
       
        await utils.send(client= client, message=message, cmd="news",msg="Zrobione! Wiadomość wysłana na {} serwery/-ów!".format(i) )
       
        
        
        #await utils.send(client= client, message=message, cmd="ann",embed=embed)