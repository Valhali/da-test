from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord

class Teest(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        try:
            await message.delete()
        except :
            pass         
        member = message.author
        url = 'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.jpeg?size=1024'.format(member)
               
        embed = discord.Embed(color=0x00ff00)
        embed.title = "test" 
        embed.description = url
        embed.set_image( url=url)
        #embed.set_author(name="ONEIRO")
        await message.channel.send(embed=embed)
        
        #await utils.upload_sett()  