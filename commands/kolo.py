from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 
import operator, discord
from random                 import randint

def podkr(t):
    r=""
    for i in t:
        if i==" ": 
            r+=" "
        else:
            r+="_"
    return r
  

def litera(t, l):
    r=""
    for i in range(0,len(t["text"])):
        if t["text"][i] == l: 
            t["cur"] = t["cur"][:i] +l + t["cur"][i+1:]
        print(i, " " , t["cur"])
    return t["cur"]

class Kolo(BaseCommand): # ilosc #kanał bot top

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        return
        conn = settings.conn
        c = settings.c
        idsrv = str(message.guild.id)
        id = str(message.channel.id)
        ch=0
        for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='kolo';", (idsrv,)):
            if j: ch = int(j[0])
        if not ch or ch==0: return        
        if int(id) != ch: return        
        try:
            await message.delete()
        except :
            pass
        txt={}   
        for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='kolo_text';", (idsrv,)):
            if j: txt = json.loads(j[0])   
            
        if not txt:    
            text = []    
            for j in c.execute("SELECT text,cat FROM kolo;"):
                text.append( [j[0], j[1]] )
            txt["text"] = text[randint(0, len(text)-1)][0].upper()      
            txt["cat"] = text[randint(0, len(text)-1)][1]      
            txt["cur"] = podkr( txt["text"]  )   
            c.execute("INSERT OR IGNORE INTO config(conf,serwer, id) VALUES (?,?,'kolo_text');", (json.dumps(txt) ,idsrv,))   
            conn.commit()       
            await utils.upload_sett()    
        if params[0] =="" : return #wyślij zasady
        
        if params[0].lower() == "kup" : #kup litere
            print("kup litere")
            return
            
        if params[0].lower() == "rank" : #ranking
            print("ranking")
            return
        
        if len(params[0])==1 : #strzel litere
            l = params[0].upper()
            if l in txt["text"] and not l in txt["cur"]:
                txt["cur"] = litera(txt, l)
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id='kolo_text' AND serwer=?;", (json.dumps(txt) ,idsrv,))   
                conn.commit()       
            else: 
                pass
        
        if len(params[0])>1 : #odgadnij haslo
            print("haslo")
            conn.commit()       
        
                
        #print(txt)
        
        embed = discord.Embed(color=0xFFFF00)
        embed.title = "Kto odgadnie hasło?"
        cat = " - "+txt["cat"] if txt["cat"] else ""
        embed.description = "`{}`".format(txt["cur"]) + cat
        await message.channel.send(embed=embed) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #gc = await utils.gc(id, "kolo", client)
        #if gc: await gc.send(odp)
        #else: await message.channel.send(odp)
            
        #embed = discord.Embed(color=0x00ff00)
        #embed.title = "Najbardziej aktywni na #{} w ostatnich {} wiadomości(ach)".format(ch.name, params[0])
        #embed.description = msg
        #await message.channel.send(embed=embed)        
        #print(top) 
        #await utils.upload_sett()  