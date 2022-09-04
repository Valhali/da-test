from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord

class Em(BaseCommand): #tytul | opis | img |thumb

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy")
            return

        try:
            await message.delete()
        except :
            pass         
            
        
        gc = await utils.gc(message.guild.id, "em", client)
        cmd = message.content[len(settings.COMMAND_PREFIX)+2:].strip()
        i = cmd.split('|')
        if not i : return
        if len(i)<2: 
            #await message.channel.send("Wybacz, że się czepiam ale nie wiem co jest tytułem a co opisem - brakuje separatora: ` | `")
            if gc: await gc.send("Wybacz, że się czepiam ale nie wiem co jest tytułem a co opisem - brakuje separatora: ` | `")
            else: await message.channel.send("Wybacz, że się czepiam ale nie wiem co jest tytułem a co opisem - brakuje separatora: ` | `")
            return
               
        embed = discord.Embed(color=0x00ff00)
        embed.title = i[0] 
        embed.description = i[1]
        if len(i)>2: 
            if i[2]: embed.set_image( url=i[2])
        if len(i)>3: 
            if i[3]: embed.set_thumbnail( url=i[3])
                        
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        