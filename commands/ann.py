from commands.base_command  import BaseCommand
import requests
import settings
import re, os, settings
import utils, discord
from discord.ext import commands

class Ann(BaseCommand): 

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if not re.findall(r'\d+',message.author.mention)[0]  == "188721035133059072": return
        try:
            await message.delete()
        except :
            pass
        
        m = message.content[len(settings.COMMAND_PREFIX)+4:]
        m = m.split("|")
        cn = m[0].split()
        
        embed = discord.Embed(color=0xFF0066)
        embed.title = m[1] 
        embed.description = m[2]
        embed.set_footer(text = message.author.display_name )
        
        for ch in cn:
            channel = client.get_channel(int(ch))
            print(channel)
            await channel.send( embed=embed  )
       
        
        
        #await utils.send(client= client, message=message, cmd="ann",embed=embed)