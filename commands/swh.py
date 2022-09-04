from commands.base_command  import BaseCommand
import urllib.request, json
import base64
import discord
import re
from xml.dom.minidom import parse, parseString
import requests, io, discord, utils
from urllib import *
from datetime import datetime, timedelta


class Swh(BaseCommand):

    def __init__(self):
        description = "Aktualne obrazy Słońca"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        msg=[]
        url=[]
        #msg.append( "Dziury koronalne")
        #url.append("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg")

        #msg.append(  "Rozbłyski słoneczne")
        #url.append("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0131.jpg")

        #msg.append( "Plamy słoneczne")
#        url.append("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg")

 #       msg.append( "Koronalny wyrzut masy")
  #      url.append("https://sohowww.nascom.nasa.gov/data/realtime/c2/1024/latest.jpg")


###############################################
        try: #averageIntensity10min.cfg  averageMagnetogram10min.cfg 
            with urllib.request.urlopen("https://gong2.nso.edu/products/tableView/getTableConfig.php?configFile=configs/hAlpha.cfg") as u:
                conf = u.read().decode()
            conf = parseString(conf) 
            age = 0
            for i in range(0,7):
                eLatestFilename =  conf.getElementsByTagName("eLatestFilename")[i].childNodes[0].data    
                eHrOffset =  conf.getElementsByTagName("eHrOffset")[i].childNodes[0].data     
                eMnOffset =  conf.getElementsByTagName("eMnOffset")[i].childNodes[0].data     
                eScOffset =  conf.getElementsByTagName("eScOffset")[i].childNodes[0].data     
                eDataSub =  conf.getElementsByTagName("eDataSub")[i].childNodes[0].data     
                eZoomSub =  conf.getElementsByTagName("eZoomSub")[i].childNodes[0].data     
                
                link = "https://gong2.nso.edu/products/tableView/getImageDetails.php?index=1&latestFile={}&hr={}&mn={}&sc={}&dataSub={}&zoomSub={}".format(eLatestFilename,eHrOffset,eMnOffset, eScOffset,eDataSub,eZoomSub  )
                
                with urllib.request.urlopen(link) as u2:
                    conf2 = u2.read().decode()
                    
                conf2 = parseString(conf2)                    
                a =  int(conf2.getElementsByTagName("age")[0].childNodes[0].data)
                
                if age==0: age = a
                if a <= age:
                    age = a
                    img =  conf2.getElementsByTagName("zoomFile")[0].childNodes[0].data
                    if len(img)<5: img = conf2.getElementsByTagName("image")[0].childNodes[0].data
                    
                    img = "https://gong2.nso.edu{}".format(img)
                conf2=None     
            msg.append( "Słońce w paśmie H-Alpha")
            url.append(img)
            
        except: pass



###############################################





        gc = await utils.gc(message.guild.id, "swh", client)

        for i in range(0,len(msg),1):
            if not msg[i]: continue
            #print(msg[i], url[i])
            try:
                if gc: await gc.send(msg[i],file= await utils.dimg(url[i],msg[i]+".jpg"))
                else: await message.channel.send(msg[i],file= await utils.dimg(url[i],msg[i]+".jpg"))
            except: 
                if gc: await gc.send("Mam problem z wczytaniem obrazu `{}`".format(msg[i]))
                else: await message.channel.send("Mam problem z wczytaniem obrazu `{}`".format(msg[i]))
            



