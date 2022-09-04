from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json, discord,re

class Ntv(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if not message.guild.id == 936626907879989248: return #naukowotv
        #if not message.guild.id == 518828593741299717: return #test
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            #await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return
        try:
            await message.delete()
        except :
            pass
        g = await client.fetch_guild(message.guild.id)

        rol = discord.utils.get(message.guild.roles,name="Widz")
        #rol = discord.utils.get(g.roles,name="Śpioch")
        u = []
        m2=[]
        for m in message.guild.members:
            if m.bot: continue
            if m.guild_permissions.send_messages:
                m2.append(m)

        for m in m2:
            if len(m.roles) <3 and rol in m.roles:
                u.append(m.mention)

            #print( m, m2[-1])

            if len(u)>1700 or m == m2[-1]:                
                embed = discord.Embed(color=0x00ff00)
                embed.title = "Ludziki bez dobranych ról"
                embed.description = " ".join(u)
                await message.channel.send(embed=embed)   
                u=[] 