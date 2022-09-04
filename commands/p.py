from commands.base_command  import BaseCommand
import requests
import re, os, settings
import utils, discord, time, re
from discord.ext import commands


class P(BaseCommand): 

    def __init__(self):
        description = ""
        params = [""]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
            
        r = re.findall('\s\S+\s?=',message.content)
        print(r)
        
        
        