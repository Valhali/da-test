from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils, hashlib, discord
from itertools import islice
from datetime import *
from dateutil.tz import *
from dateutil import tz


class Sett(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if message.author.id == client.user.id or message.author.bot:             return
        try:
            await message.delete()
        except :
            pass
        conn = settings.conn
        c = settings.c
        if params[0] =="" : return
        if not message.author.guild_permissions.administrator and not message.author.guild_permissions.kick_members and re.findall(r'\d+',message.author.mention)[0]  != "188721035133059072":
            await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
            return

        id = str(message.guild.id)
        if params[0] =="licz" : #kanal max %dopisku %odpowiedzi
            i=re.findall(r'\d+',params[1])[0]
            if len(i)==18: 
                c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("licz" , id, "licz", id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( i, "licz", id))
                if len(params)>2: 
                    j = int(params[2]) if int(params[2])>0 else 10000
                    if j:
                        c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("licz_max" , id, "licz_max", id))
                        c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( j, "licz_max", id))
                
                if len(params)>3: 
                    j = int(params[3]) if int(params[3]) in range(0,101) else 10
                    if j:
                        c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("licz_proc" , id, "licz_proc", id))
                        c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( j, "licz_proc", id))    
                if len(params)>4: 
                    j = int(params[4]) if int(params[4]) in range(0,101) else 50
                    if j:
                        c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("licz_odp" , id, "licz_odp", id))
                        print( c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( j, "licz_odp", id))    )
                conn.commit()
            if i == 0: 
                c.execute("DELETE FROM config WHERE id=? AND serwer=?);", ("licz", id))
                c.execute("DELETE FROM config WHERE id=? AND serwer=?);", ("licz_max", id))
                c.execute("DELETE FROM config WHERE id=? AND serwer=?);", ("licz_proc", id))
                c.execute("DELETE FROM config WHERE id=? AND serwer=?);", ("licz_odp", id))
                conn.commit()
                
        if params[0] =="odp" :
            i=re.findall(r'\d+',params[1])[0]
            if len(i)==18: 
                c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("odp" , id, "odp", id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( i, "odp", id))
                conn.commit()
                
        if params[0] =="limit" : # limit | komenda | czas
            msg = ' '.join([str(elem) for elem in params[1:]])
            msg = msg.split("|")
            c.execute("INSERT OR IGNORE INTO limi(komenda, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM limi WHERE komenda=? AND serwer=?);", (msg[1].strip() , id, msg[1].strip(), id))
            c.execute("UPDATE OR IGNORE limi SET czas=? WHERE komenda=? and serwer=?;", ( msg[2].strip(), msg[1].strip(), id))
            conn.commit()
            

        if params[0] =="auto" : # auto | !komenda | czas | kanal
            msg = ' '.join([str(elem) for elem in params[1:]])
            msg = msg.split("|")
            i=re.findall(r'\d+', msg[3])[0] #kanał
            
            c.execute("INSERT OR IGNORE INTO auto(komenda, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM auto WHERE komenda=? AND serwer=?);", (msg[1].strip() , id, msg[1].strip(), id))
            c.execute("UPDATE OR IGNORE auto SET czas=?, kanal=? WHERE komenda=? and serwer=?;", ( msg[2].strip(),i, msg[1].strip(), id))
            conn.commit()
            
                              # custom command
        if params[0] =="cc" : # cc komenda odpowiedź
            if "|" in message.content:#cc komenda | tytul | opis | img | th
                cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
                cmd = cmd[2:].strip()
                i = cmd.split('|')
                if not i : return
                if " " in i[0].strip():
                    await message.channel.send( message.author.mention+ " W nazwie komendy nie może być spacji. Użyj jednego słowa lub zastąp spacje np `_`  :face_with_raised_eyebrow:  ")
                    return
                if len(i)<2: 
                    await message.channel.send( message.author.mention+ " Nie rozumiem. Chyba składnie mylisz. :face_with_raised_eyebrow:  ")
                    return
                cnfid = "cmd_"+i[0].strip().lower()
                odp = {}
                cnf = {}
                for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=? LIMIT 1;", (id,cnfid) ):
                    if j: cnf=json.loads(j[0])
                           
                #print("TEST 1:" , cnf)
                odp["tyt"] = i[1].strip()[0:255]
                odp["odp"] = i[2].replace("[[","||").replace("]]", "||").strip()
                odp["img"] = i[3].strip() if len(i)>3 else ""
                odp["th"] = i[4].strip() if len(i)>4 else ""
                cnf["cnfid"] = cnfid
                
                result = hashlib.md5(message.content.encode()) 
                md5 = result.hexdigest()                        
                cnf[md5] = odp
                
                cnf = json.dumps(cnf)
                #print( "TEST 2:" ,cnf)
                #return
                c.execute("INSERT OR IGNORE INTO config(conf, serwer, id) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (cnf, id, cnfid , cnfid, id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
                conn.commit()
                    
                    
                    
            else: # stare cc
                cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
                cmd = cmd[2:].strip()
                i = cmd.split(' ', 1)
                if i : cmd = i[0].strip()
                rest = message.content.find(cmd)
                rest = message.content[rest+len(cmd):].strip()
                
                result = hashlib.md5(message.content.encode()) 
                md5 = result.hexdigest()            
                
                c.execute("INSERT OR IGNORE INTO command(cmd, srv, md5) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM command WHERE md5=? AND srv=?);", (cmd.lower(), id, md5 , md5, id))
                c.execute("UPDATE OR IGNORE command SET txt=? WHERE md5=? and srv=?;", ( rest,md5, id))
                conn.commit()

            await message.channel.send("Wygląda na to, że udało się dodać własną komendę. Aby usunąć ją - użyj komendy: `" +settings.COMMAND_PREFIX+"sett dcc "+md5+"`")
            
        if params[0] =="dcc" : # dcc md5 - usuwanie wlasnej komendy
            c.execute("DELETE FROM command WHERE md5 = ?;", ( params[1],))
            conn.commit()
              
            cnf = {}
            for j in c.execute("SELECT conf FROM config WHERE serwer=? AND conf like ?;", (id,"%"+params[1]+"%") ):
                if j: cnf=json.loads(j[0])
            if not cnf : 
                await utils.upload_sett()
                return
            cnf.pop(params[1], None)   
            cnfid=cnf["cnfid"]
            x= len(cnf)
            cnfb = cnf
            cnf = json.dumps(cnf)
            if x>1:
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
            else:
                c.execute("DELETE FROM config WHERE serwer = ? AND id=?;", (id,  cnfid))
            ######################################################################            
            cnf = {} #scc
            for j in c.execute("SELECT conf FROM config WHERE serwer=? AND conf like ?;", (id,"%"+params[1]+"%") ):
                if j: cnf=json.loads(j[0])
            if not cnf : 
                await utils.upload_sett()
                return
                                
            for k in dict(cnf["subcmd"]):
                for l in dict(cnf["subcmd"][k]):
                    if l == params[1]: 
                        cnf["subcmd"][k].pop(params[1], None)
                        print(l)
                        if not len(cnf["subcmd"][k]):
                            cnf["subcmd"].pop(k, None)
            
            cnfid=cnf["cnfid"]
            x= len(cnf["subcmd"])
            cnfb = cnf
            cnf = json.dumps(cnf)
            if x>0:
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
            else:
                c.execute("DELETE FROM config WHERE serwer = ? AND id=?;", (id,  cnfid))
            
            ######################################################################
            conn.commit()
            
            await utils.upload_sett()
            await message.channel.send("Udało się - odpowiedź usunięta!")
        
        
        
        
                              # 
        if params[0] =="horoskop" : # znak | odp
                        
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
            cmd = cmd[8:].strip()
            i = cmd.split('|', 1)
            if not i : return
            if len(i)<2: 
                await message.channel.send("Wybacz, że się czepiam ale nie wiem co jest nazwą a co opisem - brakuje separatora: ` | `")
                return
            cnfid = "horoskop_"+i[0].strip().lower()
            odp = i[1].strip()
            cnf = {}
            cnf["cnfid"] = cnfid
            for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=? LIMIT 1;", (id,cnfid) ):
                if j: cnf=json.loads(j[0])
                                
            result = hashlib.md5(odp.encode()) 
            md5 = result.hexdigest()                        
            cnf[md5] = odp
            
            cnf = json.dumps(cnf)
            #print( cnf, cnfid)
            #return
            c.execute("INSERT OR IGNORE INTO config(conf, serwer, id) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (cnf, id, cnfid , cnfid, id))
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
            conn.commit()

            await message.channel.send("Wygląda na to, że udało się dodać odpowiedź. Aby usunąć ją - użyj komendy: `" +settings.COMMAND_PREFIX+"sett dhoroskop "+md5+"`")
            
        
        
        if params[0] =="dhoroskop" : # md5 - usuwanie wlasnej komendy
            cnf = {}
            for j in c.execute("SELECT conf FROM config WHERE serwer=? AND conf like ?;", (id,"%"+params[1]+"%") ):
                if j: cnf=json.loads(j[0])
                        
            cnf.pop(params[1], None)   
            cnfid=cnf["cnfid"]
            x= len(cnf)
            cnf = json.dumps(cnf)
            if x>1:
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
            else:
                c.execute("DELETE FROM config WHERE serwer = ? AND id=?;", (id,  cnfid))
            
            conn.commit()
            await message.channel.send("Udało się - odpowiedź usunięta!")
        
        
        if params[0] =="cmd" : # komenda - wszystkie odpowiedzi do komendy + hash
            if len(params)<2: 
                await message.channel.send( message.author.mention+ " Podaj nazwę komendy!")
                return
            cnf = {}
            cnf2 = {}
            for j in c.execute("SELECT txt,md5 FROM command WHERE srv=? AND cmd=?;", (id,params[1]) ):
                if j: 
                    cnf[j[1]]= j 
            ######################        
            for j in c.execute("SELECT conf FROM config WHERE serwer=? and id=?;", (id,"cmd_"+params[1].strip().lower()) ):
                if j: 
                    j = json.loads(j[0])                       
                    for k in  islice(j, 1, None):
                        cnf[k]= (j[k]["odp"] if j[k]["odp"] else j[k]["tyt"], k)
            ######################        scc 
            for j in c.execute("SELECT conf FROM config WHERE serwer=? and id=?;", (id,"scmd_"+params[1].strip().lower()) ):
                if j: 
                    j = json.loads(j[0])                       
                    for k in  islice(j["subcmd"], 0, None):
                        for l in j["subcmd"][k]:
                            cnf[l]= (j["subcmd"][k][l]["odp"] if j["subcmd"][k][l]["odp"] else j["subcmd"][k][l]["tyt"], l)
            ########################
            
            if not cnf and not cnf2: 
                await message.channel.send( message.author.mention+ " `{:s}` - Na pewno podajesz prawidłową nazwę komendy?".format(params[1]))
                return
              
            x= len(cnf)
            msg = ""
            lk = list(cnf.keys())[-1]
            for i in cnf:
                m=cnf[i][0].replace("*","").replace("\n"," ").replace("  "," ")
                if len(m)>65: m = m[:60]+"[...]"
                msg+= "**{:s}** - `{:s}`\n".format(cnf[i][1], m)
                if len(msg)>1500 or lk == i:
                    embed = discord.Embed(color=0x00ff00)
                    embed.title = "Odpowiedzi do komendy: "+params[1]
                    embed.description = msg
                    await message.channel.send(embed=embed)
                    msg=""
            
            
            conn.commit()
        
        if params[0] =="cenz" : # cenz slowo
            cnf=[]
            for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='censore';", (id,)):
                if j: cnf = json.loads(j[0])                     
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
            cmd = cmd[4:].strip()
            if not cmd in cnf: cnf.append(cmd)
            if len(params)==1: # jesli brak słowa - wyswietl zapisane
                embed = discord.Embed(color=0x00ff00)
                embed.title = "Lista filtrów" 
                msg ="ID: filtr\n"
                for i in cnf:
                    if i: msg+= "**{}**: `{}`\n".format(cnf.index(i), i)
                embed.description = msg + "\n\n Aby usunąć jakiś filtr wpisz `{}sett dcenz ID`\nPamiętaj by za każdym razem, przed usunięciem sprawdzić ID przypisane do filtra.".format(settings.COMMAND_PREFIX)
                await message.channel.send(embed=embed)
                return
            
            try: 
                re.search(r'{}'.format(cmd), "")
            except Exception as e:
                await message.channel.send("Filtr: `{}` zawiera błędy i nie może być dodany! ```{}```".format(cmd, e))
                return
                
            cnf = json.dumps(cnf)        
            c.execute("INSERT OR IGNORE INTO config(conf, serwer, id) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (cnf, id, "censore" , "censore", id))
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, "censore", id))
            conn.commit()
            embed = discord.Embed(color=0xff0000)
            embed.description = "Filtr: `{}` dodany!".format(cmd)
            await message.channel.send(embed=embed)
    
        if params[0] =="dcenz" : # dcenz slowo // usuwanie 
            cnf=[]
            for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='censore';", (id,)):
                if j: cnf = json.loads(j[0])   
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
            cmd = cmd[5:].strip()
            a = cnf[int(params[1])]
            cnf.pop(int(params[1]))                  
            x= len(cnf)
            cnf = json.dumps(cnf)
            if x>=1:
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, "censore", id))
            else:
                c.execute("DELETE FROM config WHERE serwer = ? AND id=?;", (id,  "censore"))
            
            conn.commit()
            await message.channel.send("Udało się - Filtr: `{}` usunięty!".format(a))
        
        
        
    
                              # 
        if params[0] =="log" : # log #kanal
            if len(params)<2: return            
            i=re.findall(r'\d+', params[1])[0] #kanał
            if not i : return
            if len(i)==18: 
                c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("log" , id, "log", id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", (i, "log", id))
            if i == 0:
                c.execute("DELETE FROM config WHERE id=? AND serwer=?;", ("log", id))
            conn.commit()
        
                               # odpowiedz w wybranym kanale wyłącznie
                               # resp komenda | #kanal - pojedyncza komenda
        if params[0] =="resp" :# resp #kanal - wszystkie komendy
            if len(params)<2: return      
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip()
            cmd = cmd[4:].strip()  
            msg = "Jeśli to czytasz to oznacza, że coś się ostro popimpało w tej komendzie... ;("
            js={}
            js["def"] = 0
            js["cmd"] = {}
            for j in c.execute("SELECT conf FROM config WHERE serwer=? and id=?;", (id,"response")):
                if j: js = json.loads(j[0])  
                #print(j)
            
            if "|" in cmd:  #kanal dla komendy               
                cmd = cmd.split('|', 1)    
                if len(cmd) <2: return
                i=re.findall(r'\d+', cmd[1])[0] #kanał
                if not i: return
                if int(i) == 0 : 
                    js["cmd"].pop(cmd[0].strip())
                    msg = "Kanał odpowiedzi usnięty."
                else: 
                    js["cmd"][cmd[0].strip()] = i
                    msg = "Kanał odpowiedzi ustawiony na: {}".format(cmd[1])
            else: #kanal ogolny
                i=re.findall(r'\d+', params[1])[0] #kanał
                if not i: return
                if int(i) == 0 : 
                    js["def"] = 0
                    msg = "Główny kanał odpowiedzi usunięty"
                else: 
                    js["def"] = i
                    msg = "Główny kanał odpowiedzi ustawiony na: {}".format(params[1])
            
            js = json.dumps(js)        
            c.execute("INSERT OR IGNORE INTO config(conf, serwer, id) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (js, id, "response" , "response", id))
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( js, "response", id))
            conn.commit()
            m = await message.channel.send(msg )
            await m.delete(delay=5)
            #return
            
        if params[0] =="kolo" or params[0] =="koło": # kolo #kanal
            if len(params)<2: return            
            i=re.findall(r'\d+', params[1])[0] #kanał
            print(i)
            if not i :    return
            if len(i)==18: 
                c.execute("INSERT OR IGNORE INTO config(id, serwer) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", ("kolo" , id, "kolo", id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", (i, "kolo", id))
            if int(i) == 0:
                c.execute("DELETE FROM config WHERE id=? AND serwer=?;", ("kolo", id))
            conn.commit()
           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                              # custom sub-command
        if params[0] =="scc" : #scc komenda | subkomenda | tytul | opis | img | th
            if "|" in message.content:
                cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip() #sett
                cmd = cmd[3:].strip() #scc
                i = cmd.split('|')
                if not i : return
                if " " in i[1].strip() or " " in i[2].strip():
                    await message.channel.send( message.author.mention+ " W nazwie komendy i sub-komendy nie może być spacji. Użyj jednego słowa lub zastąp spacje np `_`  :face_with_raised_eyebrow:  ")
                    return
                if len(i)<3: 
                    await message.channel.send( message.author.mention+ " Nie rozumiem. Chyba składnie mylisz. :face_with_raised_eyebrow:  ")
                    return
                cnfid = "scmd_"+i[1].strip().lower()
                scnfid = i[2].strip().lower()
                odp = {}
                cnf = {}
                cnf["cnfid"] = cnfid
                cnf["subcmd"] = {}
                for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=? LIMIT 1;", (id,cnfid) ):
                    if j: cnf=json.loads(j[0])
                           
                #print("TEST 1:" , cnf)                
                odp={}
                odp["tyt"] = i[3].strip()[0:255]
                odp["odp"] = i[4].replace("[[","||").replace("]]", "||").strip()
                odp["img"] = i[5].strip() if len(i)>5 else ""
                odp["th"] = i[6].strip() if len(i)>6 else ""
                
                if not scnfid in cnf["subcmd"]: cnf["subcmd"][scnfid] = {}
                
                result = hashlib.md5(message.content.encode()) 
                md5 = result.hexdigest()                        
                cnf["subcmd"][scnfid][md5] = odp
                
                cnf = json.dumps(cnf)
                #print( "TEST 2:" ,cnf)
                #print( "TEST 3:" ,i)
                #return
                c.execute("INSERT OR IGNORE INTO config(conf, serwer, id) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (cnf, id, cnfid , cnfid, id))
                c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
                conn.commit()
                    
                    
            await message.channel.send("Wygląda na to, że udało się dodać własną subkomendę. Aby usunąć ją - użyj komendy: `" +settings.COMMAND_PREFIX+"sett dcc "+md5+"`")
            
        
        
        
        
        
        
        
        
        
        
        if params[0] =="slow": # slow sekundy znaki @nicki      
       
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip() #sett
            cmd = cmd[4:].strip() #slow
            cmd = cmd.split()
            slow = settings.SLOW
            if not id in slow: slow[id]={}
            
            s=int(re.findall(r'\d+', cmd[0])[0])
            z=int(re.findall(r'\d+', cmd[1])[0])
            if z<1 or z>2000: z = 2000
            
            n = []
            for i in cmd[2:]:                
                if i: n.append(int(re.findall(r'\d+', i)[0]))
            if s>0: 
                for i in n:
                    if i: 
                        slow[id][str(i)]={"s":s,"z":z,"l":0}
                        u = await client.fetch_user(int(i))
                        await message.channel.send("Ograniczenia dla **{}** zostały zapisane! Opóźnienie wysyłania wiadomości **{}** sekund, limit znaków **{}**.".format(u.name, s, z))
            else:             
                for i in n:
                    #if i in slow[id]: slow[id].pop(i)
                    if str(i) in slow[id]: 
                        slow[id].pop(str(i))
                    u = await client.fetch_user(int(i))
                    await message.channel.send("Ograniczenia dla **{}** zostały usunięte!".format(u.name))
            
            slo = json.dumps(slow)
            c.execute("INSERT OR IGNORE INTO config(conf, id) SELECT ?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? );", (slo, "slowmode" , "slowmode"))
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=?;", ( slo, "slowmode"))
        
        
        
        
        if params[0] =="calend": # calend DD-MM opis      
            dn = datetime.now(tz.gettz('Europe/Warsaw'))
            cmd = message.content[len(settings.COMMAND_PREFIX)+4:].strip() #sett
            cmd = cmd[6:].strip() #calend
            cmd = cmd.split()    
            if len(params)<2: # brak daty
                await utils.send(client= client, message=message, cmd="sett",msg="Podaj datę w formacie DD-MM!")
                return   
            opis = " ".join(params[2:]) if len(params)>1 else ""
            try:
                dn=datetime.strptime(params[1], '%d-%m').replace(year= dn.year)                
                m = int(dn.strftime("%m") )
                d = int( dn.strftime("%d"))
            except: 
                await utils.send(client= client, message=message, cmd="sett",msg="Podaj prawidłową datę w formacie DD-MM!")
                return            
            
            if len(params)==2:  #lista swiat
                embed = discord.Embed(color=0x00ff00)
                embed.title = "Lista świąt lokalnych w dniu {}".format(params[1])
                msg ="ID: opis\n"
                s=[]
                for j in c.execute("SELECT swieto FROM calendar_local WHERE server=? and day=? AND month=?;", (id,d, m)):
                    if j: s.append(j[0]) 
                    print(j)
                for i in s:
                    if i: msg+= "**{}**: `{}`\n".format(s.index(i), i)
                if msg: 
                    embed.description = msg + "\n\n Aby usunąć jakiś wpis użyj `{}sett dcalend DD-MM ID`\nPamiętaj by za każdym razem, przed usunięciem sprawdzić przypisane ID.".format(settings.COMMAND_PREFIX)
                else:
                    await utils.send(client= client, message=message, cmd="sett",msg="Nie ma wpisów na ten dzień.")
                    return
                
                
                await utils.send(client= client, message=message, cmd="sett",embed=embed)
                return    
             
                
                
            c.execute("INSERT OR IGNORE INTO calendar_local(day, month, server,swieto) VALUES ( ?,?,?,?);", (d,m,id,opis))    
            
            await utils.send(client= client, message=message, cmd="sett",msg="Wpis `{}-{}` `{}` dodany!".format(d,m,opis)   ) 
                
           
        if params[0] =="dcalend" : # dcalend DD-MM id // usuwanie 
            dn = datetime.now(tz.gettz('Europe/Warsaw'))
            try:
                dn=datetime.strptime(params[1], '%d-%m').replace(year= dn.year)                
                m = int(dn.strftime("%m") )
                d = int( dn.strftime("%d"))
            except: 
                await utils.send(client= client, message=message, cmd="sett",msg="Podaj prawidłową datę w formacie DD-MM!")
                return
            opis = []
            for j in c.execute("SELECT swieto FROM calendar_local WHERE server=? and day=? AND month=?;", (id,d, m)):
                if j: opis.append(j[0])                
            print(opis, params)
            c.execute("DELETE FROM calendar_local WHERE server = ? AND day=? AND month=? AND swieto = ?;", (id,  d, m, opis[int(params[2])]))
            
            conn.commit()
            await utils.send(client= client, message=message, cmd="sett",msg="Udało się! Wpis `{}-{}  {}` usuniety.".format(d, m, opis[int(params[2])] ))
        
          
        if params[0] == "sync":            
            if not re.findall(r'\d+',message.author.mention)[0]  == "188721035133059072":
                await message.channel.send("Za mały z Ciebie żuczek by korzystać z tej komendy ;)")
                return
            
            servers = client.guilds
            text_channel_list = []
            for s in servers:
                print(s.id, " → ", s.name)
                for ch in s.text_channels:
                    text_channel_list.append(ch) 
                    print ("\t",ch.id, " → ", ch.name)
                    if "log" in ch.name: continue
                    try:
                        messages = await ch.history(limit=100000, oldest_first=False).flatten()
                    except:
                        messages=""
                        
                    for m in messages:
                        attach=[]
                        embed=[]
                        for a in m.attachments:
                            attach.append(a.url)                    
                        attach=json.dumps(attach )
                        for a in m.embeds:
                            embed.append(a.to_dict())                    
                        embed=json.dumps(embed )
                        
                        c.execute("INSERT OR IGNORE INTO msg (msg, chan, idmsg,srv,autor,time,edit,attach,embed) VALUES (?,?,?,?,?,?,?,?,?);", (m.content,ch.id, m.id,s.id,m.author.id, m.created_at,m.edited_at, attach, embed))
                        #c.execute("UPDATE OR IGNORE msg SET msg=? WHERE idmsg=? AND srv=?;",( m.content, m.id, s.id))
                    conn.commit()  




        if params[0] == "unsub":    # !sett unsub nazwa
            if len(params)<2:
                await utils.send(client= client, message=message, cmd="sett",msg="Musisz podać nazwę kanału który chcesz odsubować np: `{}sett unsub ruda`".format(settings.COMMAND_PREFIX) )
                return

            c.execute("DELETE FROM newssub WHERE srv = ? AND news=?;", (id,  params[1].lower() ))
            
            conn.commit()
            await utils.send(client= client, message=message, cmd="sett",msg="Zapisane!")


        if params[0] == "sub":    # !sett sub nazwa #kanal        
            if len(params)<2:
                await utils.send(client= client, message=message, cmd="sett",msg="Aby dostawać info z wybranego kanału wpisz: `{}sett sub nazwa #kanał`\nGdzie `nazwa` to nazwa kanału z którego chcesz otrzymywać info a `#kanał` to miejsce gdzie ma wysyłać wiadomość. \nJeśli nie podasz #kanału to zostanie użyty ten na którym użyjesz tej komendy.".format(settings.COMMAND_PREFIX) )
                return
            cid = int(re.findall(r'\d+', params[2])[0]) if len(params)>2 else message.channel.id
            ch = client.get_channel(cid)
            sub = params[1].lower()
            
            if not ch:
                await utils.send(client= client, message=message, cmd="sett",msg="Nie mogę znaleźć takiego kanału")
                return
                
            n = False    
            n2=""
            for j in c.execute("SELECT conf FROM config WHERE id=? LIMIT 1;",("news_"+sub,)):
                if j: 
                    n = True
                    n2=j[0]
                
            if not n: # brak nazwy w bazie
                await utils.send(client= client, message=message, cmd="sett",msg="Nie mogę znaleźć takiego kanału")
                return
            
            
            c.execute("INSERT OR IGNORE INTO newssub(news, chan, srv) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM newssub WHERE news=? AND srv = ?);", (sub, cid, int(id), sub, int(id)))
            c.execute("UPDATE OR IGNORE newssub SET chan=? WHERE srv=? AND news=?;", ( cid, int(id), sub))
            
            conn.commit()  
            
            await utils.send(client= client, message=message, cmd="sett",msg="Zapisane!")
            
            if len(n2)>3:
                embed = discord.Embed(color=0xFF0066)
                embed.title = sub.capitalize()
                embed.description = n2
                await ch.send(embed=embed)
            #return




        if params[0] == "news":    # !sett news nazwa opis       
            if len(params)<2:
                await utils.send(client= client, message=message, cmd="sett",msg="Aby stworzyć nowy kanał informacyjny wpisz: `{}sett news nazwa opis`\nGdzie `opis` to pierwsza widomość wysyłana na serwer który subskrybnie Twój kanał.".format(settings.COMMAND_PREFIX) )
                return
            opis = " ".join([str(elem) for elem in params[2:]])
            nazwa = params[1].lower()
            
            
            n = False    
            for j in c.execute("SELECT id FROM config WHERE id=? AND NOT serwer=? LIMIT 1;",("news_"+nazwa, int(id) ) ):
                if j: n = True     
                
            if n: # juz takie istnieje
                await utils.send(client= client, message=message, cmd="sett",msg="Kanał o takiej nazwie już istnieje!")
                return
            
            
            c.execute("INSERT OR IGNORE INTO config(id, conf, serwer) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer = ?);", ("news_"+nazwa, opis, int(id), "news_"+nazwa, int(id)))
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE serwer=? AND id=?;", ( opis, int(id), "news_"+nazwa))
            
            
            await utils.send(client= client, message=message, cmd="sett",msg="Wygląda, że udało się wszystko zapisać.")
            
            conn.commit()  
            #return





                                    #usuwanie newslettera
        if params[0] == "dnews":    # !sett dnews nazwa       
            if len(params)<2:
                await utils.send(client= client, message=message, cmd="sett",msg="Aby usunąć kanał informacyjny wpisz: `{}sett dnews nazwa`".format(settings.COMMAND_PREFIX) )
                return
            
            nazwa = params[1].lower()
            
            
            n = False    
            for j in c.execute("SELECT id FROM config WHERE id=? AND serwer=? LIMIT 1;",("news_"+nazwa, int(id) ) ):
                if j: n = True     
                
            if not n: # juz takie istnieje
                await utils.send(client= client, message=message, cmd="sett",msg="Kanał o takiej nazwie nie istnieje (a na pewno nie na tym serwerze)!")
                return
            
            
            c.execute("DELETE FROM config WHERE id=? AND serwer = ?;", ("news_"+nazwa, int(id)))
            c.execute("DELETE FROM newssub WHERE news=?;", (nazwa, ))
            
            
            await utils.send(client= client, message=message, cmd="sett",msg="Wygląda, że udało się wszystko zapisać.")
            
            conn.commit()  
            #return


            
            
        conn.commit()    
        await utils.upload_sett()
        