from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 

class Sql(BaseCommand):

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
        conn = settings.conn
        c = settings.c
        msg = ' '.join([str(elem) for elem in params])
        
        c.execute(msg)
        conn.commit()  
         
        #await utils.upload_sett()  