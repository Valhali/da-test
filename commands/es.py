from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, pprint
from datetime import datetime
import utils 
import operator, discord

class Es(BaseCommand): # 

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        #if re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072": return
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return
        try:
            await message.delete()
        except :
            pass
        ch = re.findall(r'\d+',params[1])[0]
        ch = client.get_channel(int(ch) )
        msg = await ch.fetch_message(int(params[0]) )
        em = msg.embeds
        s=""
        for e in em:
            s += "`{}`\n".format( e.to_dict() )
                    
        embed = discord.Embed(color=0x00ff00)
        #embed.title = "Serwery z Rudą"
        embed.description = s
        await message.channel.send(embed=embed)        
        #print(top) 
        #await utils.upload_sett()  