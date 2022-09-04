from matplotlib.font_manager import json_dump
from commands.base_command  import BaseCommand
import urllib.request, json
import base64
import discord
import re
import requests, io, discord, utils, time, settings
from datetime import datetime, timedelta
from dateutil.tz import *
from random                 import randint
import os
from urllib.parse import urlparse
from pytube import YouTube 
#from tabulate import tabulate

class Nasa(BaseCommand):

    def __init__(self):
        description = "Różne rzeczy z NASA"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        
        embed = discord.Embed(color=0x0066ff)
        embed.title = "Dostępne sub-komendy:"        
        embed.description = """`apod` - Astronomiczne zdjęcie dnia. Losowe lub dopisując datę w formacie YYYY-MM-DD zobaczysz zdjęcie z konkretnego dnia.
        `neo` - Przeloty obiektów bliskich ziemi.
        `info nazwa_łazika` - Info o łazikach marsjańskich.
        `photo nazwa_łazika` - Zdjęcia z łazików marsjańskich. Można dodać datę.
        Więcej komend w przyszłości.
        """
        rover = {"spirit": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Rover1.jpg/1024px-Rover1.jpg", "opportunity":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Opportunity_PIA03240.jpg/1280px-Opportunity_PIA03240.jpg", "curiosity":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Mars_%27Curiosity%27_Rover%2C_Spacecraft_Assembly_Facility%2C_Pasadena%2C_California_%282011%29.jpg/1280px-Mars_%27Curiosity%27_Rover%2C_Spacecraft_Assembly_Facility%2C_Pasadena%2C_California_%282011%29.jpg", "perseverance":"https://ocdn.eu/images/pulscms/ZmI7MDA_/b2a569e00119c348528e2c8f22d8cbb3.jpg"}
                    
        if not params[0]:
            await utils.send(client= client, message=message, cmd="nasa",embed=embed )
            return
        d=""
        if params[0].lower() == "apod":
            if len(params)>1:
                p1 = message.content[len(settings.COMMAND_PREFIX)+9:].strip()
                try:
                    p2=datetime.strptime(p1, '%Y-%m-%d')
                except:   
                    try:
                        p2=datetime.strptime(p1, '%Y.%m.%d')
                    except:   
                        try:
                            p2=datetime.strptime(p1, '%d.%m.%Y')
                        except:   
                            try:
                                p2=datetime.strptime(p1, '%d-%m-%Y')
                            except: 
                                try:
                                    p2=datetime.strptime(p1, '%Y %m %d')
                                except:     
                                    try:
                                        p2=datetime.strptime(p1, '%d %m %Y')
                                    except:     
                                        await utils.send(client= client, message=message, cmd="nasa",msg="Podaj datę w formacie `YYYY-MM-DD` lub `DD-MM-YYY`" )
                                        return

                
                
                if datetime.timestamp(datetime.now(tzutc())) < datetime.timestamp(p2):
                    await utils.send(client= client, message=message, cmd="nasa",msg="Nie wiem co wybiorą w przyszłości - spróbuj podać inną datę." )
                    return
                d = "&date=" + p2.strftime("%Y-%m-%d")  if len(params)>1 else "" 
            
            url= "https://api.nasa.gov/planetary/apod?api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X&count=1"
            if d: url = "https://api.nasa.gov/planetary/apod?api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X" +d
            
            r = requests.get(url, allow_redirects=True).content
            
            j = json.loads(r)
            k = j if d else j[0]
            typ = k["media_type"]
            img = k["hdurl"] if "hdurl" in k else k["url"]    
            autor = k["copyright"] if "copyright" in k else ""
            
            vid = ""
            file=''
            embed.title = k["title"]      
            embed.description = k["explanation"]
            embed.set_footer(text="{}  {}".format(k["date"], autor) )    
            #if typ=="image": embed.set_image(url=img )   
            if typ=="image":             
                a = urlparse(img)            
                n=os.path.basename(a.path)
                file= await utils.dimg(img,n)    
                embed.set_image(url="attachment://"+n) 
                try:
                    await utils.send(client= client, message=message, cmd="nasa",embed=embed, file=file  )    
                except:
                    embed.set_image(url=k["url"]) 
                    await utils.send(client= client, message=message, cmd="nasa",embed=embed  )   
                    
            if typ=="video": 
                vid="\n" + img                     
                yt = YouTube(img) 
                embed.set_image(url=yt.thumbnail_url )
                #print(yt.thumbnail_url.replace("sddefault.jpg","maxresdefault.jpg"))
                
                embed.description = k["explanation"] +vid
                await utils.send(client= client, message=message, cmd="nasa",embed=embed )
            return          
            
            
        if params[0].lower() == "neo":
            d1 = datetime.now(tzutc())
            t1 = d1.strftime("%Y-%m-%d") 
            t2 = (d1 + timedelta(hours=+24)).strftime("%Y-%m-%d") 
            url= "https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X".format(t1, t2)
            r = requests.get(url, allow_redirects=True).content
            j = json.loads(r)
            
            #print(sorted(j["near_earth_objects"][t1]["close_approach_data"][0]["epoch_date_close_approach"].items(),key=lambda x:x[1] ))
            #return
            opis = ""
            k = [t1, t2]
            for t in k:
                for i in j["near_earth_objects"][t]:
                    if len(opis)>1950: break
                    name = i["name"].replace("(","").replace(")","")
                    #mag = i["absolute_magnitude_h"]
                    size = "{:.1f}x{:.1f}m".format(i["estimated_diameter"]["meters"]["estimated_diameter_min"], i["estimated_diameter"]["meters"]["estimated_diameter_max"])
                    hazard = "TAK" if i["is_potentially_hazardous_asteroid"] else "NIE"
                    ti = i["close_approach_data"][0]["epoch_date_close_approach"]
                    ti = datetime.fromtimestamp(int(ti)/1000)                
                    ti = ti.strftime("%d-%m %H:%M") 
                    kms = i["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]
                    lun = i["close_approach_data"][0]["miss_distance"]["lunar"]
                    
                    opis += "→{} - **{}** - {:.1f}km/s - {:.1f}LD - {} - PHA: {}\n".format(ti, name, float(kms), float(lun),size, hazard )
            #print(tabulate([[name, mag, hazard]], headers=['Nazwa', 'mag', "Niebezpieczna"]))
             
            embed.title = "Neo - Near Earth Object"  
            embed.description = opis
            embed.set_footer(text="*PHA - Potencjalnie niebezpieczny\n*LD - Lunar Distance".format(t1, t2) )   

            await utils.send(client= client, message=message, cmd="nasa",embed=embed )
            return            
       
       
        if params[0].lower() == "info": 
            
            if len(params)<2: 
                await utils.send(client= client, message=message, msg="Podaj prawidłową nazwę łazika!\n `perseverance, curiosity, opportunity, spirit`", cmd="nasa" )
                return  
            params[1]  = params[1].lower()
            if  not params[1] =="perseverance" and not params[1] =="curiosity" and not params[1] =="opportunity" and not params[1] =="spirit":
                
                await utils.send(client= client, message=message, msg="Podaj prawidłową nazwę łazika!\n `perseverance, curiosity, opportunity, spirit`", cmd="nasa" )
                return  
                
            url= "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/?api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X".format(params[1])
            r = requests.get(url, allow_redirects=True).content
            j = json.loads(r)
            cam = []
            for i in j["rover"]["cameras"]:
                if i: cam.append(i["full_name"])
            cam = ", ".join(cam)    
            opis = """Start: {}
            Lądowanie: {}
            Status: {}
            Ilość zdjęć: {}
            Kamery ({}): {}""".format(j["rover"]["launch_date"], j["rover"]["landing_date"], j["rover"]["status"], j["rover"]["total_photos"], len(j["rover"]["cameras"]), cam)
            
            
                        
            embed.title = j["rover"]["name"]
            embed.description = opis
            embed.set_thumbnail(url = rover[params[1]])

            await utils.send(client= client, message=message, cmd="nasa",embed=embed )
            return            
       
        if params[0].lower() =="photo": #photo
       
            if len(params)<2: 
                await utils.send(client= client, message=message, msg="Podaj prawidłową nazwę łazika!\n `perseverance, curiosity, opportunity, spirit`", cmd="nasa" )
                return  
            params[1]  = params[1].lower()
            if  not params[1] =="perseverance" and not params[1] =="curiosity" and not params[1] =="opportunity" and not params[1] =="spirit":
                
                await utils.send(client= client, message=message, msg="Podaj prawidłową nazwę łazika!\n `perseverance, curiosity, opportunity, spirit`", cmd="nasa" )
                return  
            d=""    
            if len(params)>2:
                p1 = params[2]
                try:
                    p2=datetime.strptime(p1, '%Y-%m-%d')
                except:   
                    try:
                        p2=datetime.strptime(p1, '%Y.%m.%d')
                    except:   
                        try:
                            p2=datetime.strptime(p1, '%d.%m.%Y')
                        except:   
                            try:
                                p2=datetime.strptime(p1, '%d-%m-%Y')
                            except:                                     
                                await utils.send(client= client, message=message, cmd="nasa",msg="Podaj datę w formacie `YYYY-MM-DD` lub `DD-MM-YYY`" )
                                return

                
                
                if datetime.timestamp(datetime.now(tzutc())) < datetime.timestamp(p2):
                    await utils.send(client= client, message=message, cmd="nasa",msg="Nie wiem co będzie w przyszłości - spróbuj podać inną datę." )
                    return
                
                d = p2.strftime("%Y-%m-%d") if len(params)>2 else "" 
            d2 = d    
            url= "https://api.nasa.gov/mars-photos/api/v1/manifests/{}/?api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X".format(params[1])
            r = requests.get(url, allow_redirects=True).content
            j = json.loads(r)
            d = "earth_date="+d if d else "earth_date="+ j["photo_manifest"]["max_date"]
            if not d2: d2 = j["photo_manifest"]["max_date"]
            lp = j["photo_manifest"]["max_date"]
            st = j["photo_manifest"]["status"]
            tp = j["photo_manifest"]["total_photos"]
            ln = j["photo_manifest"]["landing_date"]
            sm = j["photo_manifest"]["launch_date"]
            sol = j["photo_manifest"]["max_sol"]
            
            url= "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?{}&api_key=GSONPs07hZP9E1gX5UUsdmy4pezOVdDiiIhwQg2X".format(params[1], d)
            r = requests.get(url, allow_redirects=True).content
            j2 = json.loads(r)
       
            p = len(j2["photos"])
            if p <1:                 
                await utils.send(client= client, message=message, cmd="nasa",msg="Brak zdjęć z podanego dnia :frowning: " )
                return
            l = randint(0,p-1)
            if len(params)>3:
                if params[3].isnumeric() and 0 < int(params[3]) <= p : l = int(params[3])-1
           
            embed.title = "{} (zdjęcie: {}/{})".format(j["photo_manifest"]["name"] , l+1, p  )
            embed.description ="""Najnowsze dostępne zdjęcia: {} (sol: {})
            Status: {}
            Wszystkich zdjęć: {}
            Start misji: {}
            Lądowanie: {}""".format(lp,sol, st,tp, sm, ln)
            embed.set_image(url=j2["photos"][l]["img_src"])
            embed.set_thumbnail(url=rover[params[1]])
            embed.set_footer(text = "{} - {}".format( d2, j2["photos"][l]["camera"]["full_name"]))
            
            await utils.send(client= client, message=message, cmd="nasa",embed=embed )
            return
            
       
       
        if params[0].lower() =="jwst":
            r = requests.get("https://api.jwstapi.com/program/list?", allow_redirects=True, headers={"X-API-KEY":settings.JWST_API} ).content
            j2 = json.loads(r)
           # with open('jwst.json', 'w') as f:
           #     json.dump(j2, f)
            for i in j2["body"]:
                print( i,"\n\n")
            return
       
       
       ##################################################################
        await utils.send(client= client, message=message, cmd="nasa",embed=embed )








