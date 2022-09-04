from commands.base_command  import BaseCommand
import requests
import settings
import re, os, settings
import utils, discord, sys
from discord.ext import commands

class Ver(BaseCommand): 

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
        
        appinfo = await client.application_info()
        print(discord.__version__)
        print(sys.version_info)
        print(appinfo.cover_image_url_as( format='jpg' ))
        print(appinfo.icon_url_as( format='jpg' ))
       
        
        return
    
        embed = discord.Embed(color=0xFF0066)
        embed.title = "" 
        embed.description = ""
        #embed.set_footer(text = message.author.display_name )
        
        await channel.send( embed=embed  )
       
        
        
        #await utils.send(client= client, message=message, cmd="ann",embed=embed)