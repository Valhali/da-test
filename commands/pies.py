from commands.base_command  import BaseCommand
import json
import discord
import re
import requests, io, discord, utils, settings




class Pies(BaseCommand):

    def __init__(self):
        description = "Losowe zdjęcia psów"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
            
        if params[0]: 
            breed = message.content[6:].strip().lower()        
            r = requests.get(settings.DOG_API_URL + "v1/breeds/search?q={}".format(breed), headers={"X-API-KEY":settings.CAT_API_KEY} )            
            js = json.loads(r.content)
            if not js:                
                r = requests.get(settings.DOG_API_URL + "v1/breeds?attach_breed=0", headers={"X-API-KEY":settings.CAT_API_KEY} )            
                js = json.loads(r.content)
                rasy=[]
                for i in js:
                    rasy.append( i["name"])           
                m = "Nie mogę znaleźć takiej rasy ;(\nSpróbuj: " 
                rp=True
                for i in rasy:
                    if rp: 
                        m = m+i
                        rp=False
                    else: m = m+", "+i
                    if len(m)>1950 or i == rasy[-1]: 
                        await utils.send(client= client, message=message, cmd="pies",msg=m)
                        m=""
                        rp=True
                return
                
            bid= js[0]["id"]    
            r = requests.get(settings.DOG_API_URL + "v1/images/search?size=full&sub_id={}&limit=1&breed_id={}".format(message.author.id, bid), headers={"X-API-KEY":settings.CAT_API_KEY} )
            
        else:
            r = requests.get(settings.DOG_API_URL + "v1/images/search?size=full&sub_id={}&limit=1".format(message.author.id), headers={"X-API-KEY":settings.CAT_API_KEY} )
        
        
        js = json.loads(r.content)
        #print(js)
        info = []
        if "breeds" in js[0] :
            info = js[0]["breeds"]
        if info: info = info[0]
        #print(js)
        
        d=""
        t=""
        if "name" in info: t = info["name"]
        if "alt_names" in info: 
            if t: t =t+" ("+ info["alt_names"]+")"
            else: t = info["alt_names"]
        
        if "weight" in info: d=d +"\n**Waga**: {}kg".format( info["weight"]["metric"])
        if "height" in info: d=d +"\n**Wysokość**: {}cm".format( info["height"]["metric"])
        if "temperament" in info: d=d +"\n**Temperament**: {}".format( info["temperament"])
        if "origin" in info: d=d +"\n**Pochodzenie**: {}".format( info["origin"])
        if "bred_for" in info: d=d +"\n**Zastosowanie**: {}".format( info["bred_for"])
        if "description" in info: d=d +"\n**Opis**: {}".format( info["description"])
        if "life_span" in info: d=d +"\n**Długość życia**: {} lat".format( info["life_span"].replace("years","") )
        if "wikipedia_url" in info: d=d +"\n[Wikipedia]({})".format( info["wikipedia_url"])
        if "cfa_url" in info: d=d +"\n[The Cat Fanciers’ Association]({})".format( info["cfa_url"])
        if "vetstreet_url" in info: d=d +"\n[Vetstreet]({})".format( info["vetstreet_url"])
            
        
        
        embed = discord.Embed(color=0x888888)
        embed.title = t
     
        embed.set_image(url=js[0]["url"]) 
                        
        embed.description =  d
        await utils.send(client= client, message=message, cmd="pies",embed=embed )







