from commands.base_command  import BaseCommand
import urllib.request, json, urllib.parse
import base64
import discord, utils, settings
from urllib import *
from py_expression_eval import Parser

class Oblicz(BaseCommand):

    def __init__(self):
        description = "Kalkulator"
        params = ["równanie"]
        super().__init__(description, params)

    async def handle(self, params, message, client):


        cmd = message.content[len(settings.COMMAND_PREFIX)+6:].strip()
        if not cmd : return
        
        gc = await utils.gc(message.guild.id, "oblicz", client)
        
        
        parser = Parser()
        try:
            a = parser.parse(cmd)
        except:
            msg = message.author.mention + " Nie mam pojęcia co z tym zrobić :frowning: Upewnij się, że to poprawna składnia."
            
            if gc: await gc.send(msg)
            else: await message.channel.send(msg)
            return
            
        try:
            msg = a.evaluate({})
            msg = "`{}` = `{}`".format( a ,msg) 
        except:
            msg = "`{}` = `{}`".format(cmd, a.simplify({}).toString())

        
        embed = discord.Embed(color=0xffff00)
        embed.description = msg
        
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        
        try:
            await message.delete()
        except :
            pass


