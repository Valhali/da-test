from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib, settings
from random                 import randint
from datetime import datetime, timedelta
import utils, discord, time
from bs4 import BeautifulSoup
from discord.ext import commands

#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

class B(BaseCommand): 

    def __init__(self):
        description = "Info o przelotach satelit."
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        return
        gc = await utils.gc(message.guild.id, "b", client)
        msg = ""
                      
        ddb = DiscordComponents(client)
   
   
        comp = [
                [
                Button(style=ButtonStyle.red, label="Tak!"),
                Button(style=ButtonStyle.green, label="Nie"),
                Button(style=ButtonStyle.blue, label="Lubię placki")
                ],
            ]
            
        embed = discord.Embed(color=0x00ff00)
        embed.description = "Czy ananas + pizza = abominacja?"
        await message.channel.send(
            embed=embed,
            components=comp,
        )
        print( {"components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "Click me!",
                    "style": 1,
                    "custom_id": "click_one"
                }
            ]

        }
    ]} )
        # "{'type': 2, 'style': 1, 'label': 'Blue', 'custom_id': '3bd3f6eb-bf94-11eb-8ff7-001b10002aec', 'url': None, 'disabled': False}"
        #return
        while 1:
            res = await ddb.wait_for("button_click")
            if res.channel == message.channel:
                m = await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f'{res.component.label} clicked'
                )
                print(res.component)
                if m: m.delete(delay=3)
        
        return                 
        help_embed = discord.Embed.from_dict(help_commands)
        await message.channel.send(embed=help_embed)

        return
        
        embed = discord.Embed(color=0x00ff00)
        #embed.title = "Przeloty satelit dla miejscowości {}".format(n) 
        embed.description = iss
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        #await utils.upload_sett()  