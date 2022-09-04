from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json, discord
from mee6_py_api import API
import math, re , utils


class Mee(BaseCommand):

    def __init__(self):
        description = "Oblicz ile brakuje Ci do wybranego poziomu w bocie Mee6"
        params = ["poziom"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        id = str(message.guild.id)
       
       
       ############################################
       
        min_xp_gain_per_message = 15;
        max_xp_gain_per_message = 25;

        
        desired_level = int(re.findall(r'\d+',params[0])[0])
       
        if not desired_level:
            return
       
        channel = message.channel        
        mee6API = API(id)      
        
        i = 0
        while 1: 
            leaderboard_page = await mee6API.levels.get_leaderboard_page(i)
            i+=1
            if not leaderboard_page["players"]: break
            for j in leaderboard_page["players"]:
                if int(j["id"]) == message.author.id:      
                    current_xp = j["detailed_xp"][2]
                    break
            if current_xp: break        
                    


        xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91);
        xp_needed = xp_to_desired_level - current_xp;

        if xp_needed < 0:
            await message.channel.send("Gratuluję! Już masz już poziom. Mogę obliczyć ile potrzebujesz do wyższego poziomu.")
            return
        
        min_messages_needed_to_send = math.ceil(xp_needed / max_xp_gain_per_message);
        avg_messages_needed_to_send = math.ceil(xp_needed / ((min_xp_gain_per_message + max_xp_gain_per_message) / 2));
        max_messages_needed_to_send = math.ceil(xp_needed / min_xp_gain_per_message);

       ############################################
                
                
        msg = "**{}** do wbicia **{}** poziomu potrzebujesz jeszcze **{}** XP.\n\nW przeliczeniu na wiadomości będzie to\nMinimum: **{}**\nŚrednio: **{}**\nMax: **{}**".format(message.author.mention, desired_level, int(xp_needed) ,min_messages_needed_to_send, avg_messages_needed_to_send, max_messages_needed_to_send )
                
                
        gc = await utils.gc(id, "mee", client)
        embed = discord.Embed(color=0xFFFF00)
        embed.title = "Mee6"
        embed.description = msg
        embed.set_footer(text = "XP w ilości 15-25 dostajesz tylko raz na minutę!")
        embed.set_thumbnail (url=str(message.author.avatar_url_as(static_format ="jpg",size =1024)))
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)        
                
                
                
                
                
                