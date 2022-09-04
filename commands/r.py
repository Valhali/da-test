from commands.base_command  import BaseCommand
import urllib.request, json, urllib.parse
import base64
import discord, utils, settings
from urllib import *


class R(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):


        cmd = message.content[len(settings.COMMAND_PREFIX)+1:].strip()
        if not cmd : return
        cmd = urllib.parse.quote(cmd)
        #print(cmd)
        #cmd = cmd.encode('utf-8')
        #print(cmd)
        
        d1 = {}
        with urllib.request.urlopen("http://api.brainshop.ai/get?bid=155995&key=am2cyEEs9gMcELCt&uid={}&msg={}".format(message.author.id, cmd)) as url:
            d1 = url.read().decode()
        
        d1 = json.loads(  d1  )
        
        gc = await utils.gc(message.guild.id, "r", client)
        if gc:
            if gc.id == message.channel.id:
                await message.reply(d1["cnt"]) 
            else:
                await gc.send(message.author.mention +" - "+d1["cnt"])
                try:
                    await message.delete()
                except :
                    pass
        else:
            await message.reply(d1["cnt"]) 


