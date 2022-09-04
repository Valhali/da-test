from commands.base_command  import BaseCommand
import urllib.request, json, utils
import base64
import discord, settings
import re
import requests
from bs4 import BeautifulSoup
from dateutil import tz
from dateutil.tz import *
from datetime import datetime, timedelta, time


class Przypominajka(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        conn = settings.conn
        c = settings.c
        try:
            await message.delete()
        except :
            pass
        cnf = []
        y = str(datetime.now(tzutc()).year )
        now = str( datetime.now(tzutc()).strftime("%d %b %Y %H:00 UT") )
        past = datetime.now(tzutc()) + timedelta(hours=-1)
        past = str( past.strftime("%d %b %Y %H:00 UT") )
        
        for j in c.execute("SELECT cnf FROM reminder WHERE date=? LIMIT 1;", (now,) ):
            if j: cnf = json.loads(j[0])
        
        
        
        
        embed = discord.Embed(color=0x0000FF)
        embed.title = proc
        embed.description = msg
        embed.set_thumbnail(url=url)
        #embed.set_image(url=url)
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "przypominajka", client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)








