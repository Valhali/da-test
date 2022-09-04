from commands.base_command  import BaseCommand
import urllib.request, json, urllib.parse
import base64
import discord, utils
from urllib import *


class Sw(BaseCommand):

    def __init__(self):
        description = "Info o wietrze słonecznym"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        d1 = {}
        with urllib.request.urlopen("https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json") as url:
            d1['d'] = url.read().decode()
        
        #d1 = json.dumps(  d1  )
        
        #d1 = str(d1)
        d1 = urllib.parse.urlencode(d1)
        d1 = d1.encode('utf-8')
        #print(d1)
                
        with urllib.request.urlopen("https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json") as url:
            data = json.loads(url.read().decode())
            data.pop(0)
        j = len(data)-1
        ud = ["","","",""]
        ma=[[0,0,0,0],[0,0,0,0],[0,0,0,0]] # gestosc predskosc temp
        for i in data: #znajdz rekordy            
            if i[1] is not None:
                if float(ma[0][1]) < float(i[1]) : ma[0] = i
            if i[2] is not None:
                if float(ma[1][2]) < float(i[2]) : ma[1] = i
            if i[3] is not None:
                if float(ma[2][3]) < float(i[3]) : ma[2] = i
            
        for i in range (1,4):    
            if float(data[j][i]) > float(data[j-1][i]) : ud[i-1] = "↑"
            if float(data[j][i]) < float(data[j-1][i]) : ud[i-1] = "↓"
        
        
        str1 = ""
        str1 += "Gęstość: " + ud[0] + " " + data[j][1] +" proton/cm³\n"
        str1 += "Prędkość: " + ud[1] + " " + data[j][2] +" km/s\n"
        str1 += "Temperatura: " + ud[2] + " " + data[j][3] +" °K\n"
       
        msg = str1


        str1 = ""
        str1 += "Gęstość: "+  str(ma[0][0]).replace(":00.000"," UTC") +" → " +  str(ma[0][1]) +" proton/cm³\n"
        str1 += "Prędkość: " + str(ma[1][0]).replace(":00.000"," UTC") +" → " + str(ma[1][2]) +" km/s\n"
        str1 += "Temperatura: " + str(ma[2][0]).replace(":00.000"," UTC") +" → " + str(ma[2][3]) +" °K\n"
        #msg += str1

        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name="Wiatr słoneczny (" + data[j][0].replace(":00.000"," UTC") +")", value=msg, inline=False )
        embed.add_field(name="Rekordy tygodnia", value=str1, inline=False )
        
        #return
        #await message.channel.send(msg)
        #=============================================
        
        
        
        req =  request.Request(url="http://valhali.5v.pl/bocinka/chart/mod/", data=d1, method="POST")
        #req =  request.Request(url="http://localhost/bocinka/chart/mod/", data=d1, method="POST")
        #req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as url:
            b64 = url.read().decode()
            #print(b64)
            data = base64.b64decode(b64)
            #data = json.loads(url.read().decode())
            #data = base64.b64decode(data)

        f = open("img\\all.png", "wb")
        f.write(data)
        f.close()
        #with open('img\\all.png', 'rb') as fp:    
           # if gc: await gc.send(file=discord.File(fp, 'all.png'))
           # else: await message.channel.send(file=discord.File(fp, 'all.png'))
        #=============================================
        with open('img\\all.png', 'rb') as fp: 
            file=discord.File(fp, 'all.png')
        embed.set_image(url="attachment://all.png")

        
        await utils.send(client= client, message=message, cmd="sw",embed=embed, file=file )


