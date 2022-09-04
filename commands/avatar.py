from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import discord, utils

class Avatar(BaseCommand):

    def __init__(self):
        description = "Pokaż duży avatar"
        params = ["@wzmianka"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        av=""
        if (message.mentions.__len__()>0):
            for user in message.mentions:
                #av = user.avatar_url
                av = user.avatar_url_as(static_format ="jpg",size =1024)
                #await message.channel.send(user.avatar_url)
        if (message.mentions.__len__()==0):
            #av = message.author.avatar_url
            av = message.author.avatar_url_as(static_format ="jpg",size =1024)
            #await message.channel.send(message.author.avatar_url)
            
            
        if not av: return    
        embed = discord.Embed(color=0x00ff00)
        embed.set_image(url=av)
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "avatar", client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
