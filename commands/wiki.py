from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import wikipedia, discord

class Wiki(BaseCommand):

    def __init__(self):
        description = "Wstawka z wikipedii. Wpisz np: "+settings.COMMAND_PREFIX+"wiki oneironautyka"
        params = ["tekst"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        l1 = ["pl","en"]    
        if params:
            m = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
            if "|" in m: 
                l1=[]
                l2 = m.split("|")
                l1.append(l2[0].strip())
                msg = l2[1].strip()
            else: msg = ' '.join([str(elem) for elem in params])
            
            m = m2 = i =im =""
            gc = await utils.gc(message.guild.id, "wiki", client)
            for l in l1:
                wikipedia.set_lang(l)
                try: 
                    m = wikipedia.page(msg,auto_suggest=True, redirect=True,preload=True) 
                    i = m.images
                    for img in i:
                        if img[-3:]== "jpg" or img[-4:]== "jpeg" or img[-3:]== "gif" or img[-3:]== "png" or img[-3:]== "bmp":
                            #print(img)
                            im=img
                            break
                    m2 = wikipedia.summary(m.title,sentences=3,chars=1500)   
                except :
                    pass   
                if m: break
            
            if not m : 
                #await message.channel.send("Coś nie mogę tego znaleźć, spróbuj wpisać inaczej.")
                if gc: await gc.send("Coś nie mogę tego znaleźć, spróbuj wpisać inaczej.")
                else: await message.channel.send("Coś nie mogę tego znaleźć, spróbuj wpisać inaczej.")
                return
            #await message.channel.send("**"+m.title+ "** ```" +m2+"```Więcej doczytasz tu: "+m.url)
         
         
        embed = discord.Embed(color=0x00ff00)
        embed.title = m.title 
        embed.description = m2
        if im : embed.set_thumbnail(url=im)
        embed.add_field(name="Źródło:", value="Więcej doczytasz [>tutaj<]({:s})".format(m.url) )
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        #await utils.upload_sett()  