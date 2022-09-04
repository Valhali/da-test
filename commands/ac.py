from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json

class Ac(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        msg = []
        msg.append(' '.join([str(elem) for elem in params]))
        js = {"ciekawostki":msg}

        url = 'https://do-liczyk.sourceforge.io/bocinka/'
        body = 'c='+json.dumps(js)
        headers = {'content-type' : 'application/x-www-form-urlencoded'}



        r = requests.post(url, data=body, headers=headers)
        #print(r.content)




            #await message.channel.send(msg)
