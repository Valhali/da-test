from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, discord

class Ankieta(BaseCommand): #ankieta tytuł | opis | emotek opcja | emotek2 opcja2 ...

    def __init__(self):
        description = "Ankieta / głosowanie"
        params = ["tytuł | opis | emotek opcja | emotek2 opcja2"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass         
        h = "Prawidłowa składnia to: \n`{}ankieta tytuł | opis | :emotek1: opcja1 | :emotek2: opcja2` \nnp: \n`{}ankieta Głosujemy | Hawajka to pizza? | :white_check_mark: TAK | :x: NIE | :pancakes: Lubię placki`".format( settings.COMMAND_PREFIX,settings.COMMAND_PREFIX)        
        
        cmd = message.content[len(settings.COMMAND_PREFIX)+7:].strip()
        if not cmd : 
            embed = discord.Embed(color=0x005500)
            embed.title = "Błąd!"
            embed.description = h     
            await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
            return
        cmd = cmd.split("|")
        
        be=False
        try:
            if not cmd[2].strip(): be = True #bez emotkow
        except:pass
        if len(cmd)==1 or be: 
            embed = discord.Embed(color=0x005500)
            embed.title = "Błąd! Brak emotków i/lub opisu opcji!"
            embed.description = h        
            await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
            return
       
        if len(cmd)<4:
            embed = discord.Embed(color=0x005500)
            embed.title = "Błąd! Dobra ankieta musi mieć min. 2 opcje do wyboru!"
            embed.description = h        
            await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
            return
       
        msg = cmd[1].strip() +"\n"
        emot = []
        for e in  cmd[2:]:
            if not e: 
                embed = discord.Embed(color=0x005500)
                embed.title = "Błąd! Opis opcji nie może być pusty!"
                embed.description = h        
                await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
                return
            f = e.split()
            if f: 
                g = e.replace(f[0].strip(),"").strip()
                if not g or not f[0].strip():                           
                    embed = discord.Embed(color=0x005500)
                    embed.title = "Błąd! Opis opcji nie może być pusty!"
                    embed.description = h        
                    await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
                    return
                msg+="\n {} - {}".format(f[0].strip(), g)
                if await utils.emojiavail(message.guild, f[0].strip() ):
                    emot.append(f[0].strip())
                else:                    
                    embed = discord.Embed(color=0x005500)
                    embed.title = "Błąd! Emoty tylko standardowe + serwerowe!"
                    embed.description = h        
                    await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
                    return
                    
            else:                               
                embed = discord.Embed(color=0x005500)
                embed.title = "Błąd! Opis opcji do poprawki!"
                embed.description = h        
                await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
                return
                
        embed = discord.Embed(color=0xccff00)
        try:
            embed.set_footer(text = "Autor ankiety: {}".format(message.author.display_name))
        except:pass
        embed.title = cmd[0].strip()        
        embed.description = msg
        #m = ""
        m = await utils.send(client= client, message=message, cmd="ankieta",embed=embed)
        for i in emot:
            if not i: continue
            try:  await m.add_reaction(i) 
            except:pass
       
       
       
       
       
       