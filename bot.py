import sys
from pprint import pprint
import settings, utils
import json
import requests
import discord, random
import message_handler
from discord.ext.commands import Bot, has_permissions, CheckFailure
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event              import BaseEvent
from events                         import *
from multiprocessing                import Process
import os, time, re
from random                 import randint
import TenGiphPy
from datetime import *
from dateutil.tz import *
from dateutil import tz
  
#from discord_slash import SlashCommand
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
settings.BOT_TOKEN = os.getenv('BOT_TOKEN')
print(settings.BOT_TOKEN)

conn = settings.conn
c = settings.c
bot_id = "573821635677913108"
# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()

API_KEY = settings.API_KEY
SEARCH_ENGINE_ID = settings.SEARCH_ENGINE_ID
        
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
        #print(i, " " , t["cur"])
    return t["cur"]


async def kolo(message, client):
    params = message.content.split()
    if not params: return  
    conn = settings.conn
    c = settings.c
    idsrv = str(message.guild.id)
    id = str(message.channel.id)
    ch=0
    for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='kolo';", (idsrv,)):
        if j: ch = int(j[0])
    if not ch or ch==0: return        
    if int(id) != ch: return        
    
    txt={}   
    for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='kolo_text';", (idsrv,)):
        if j: txt = json.loads(j[0])   
        
    if not txt:    
        text = []    
        for j in c.execute("SELECT text,cat FROM kolo;"):
            text.append( [j[0], j[1]] )
        ri = randint(0, len(text)-1)
        txt["text"] = text[ri][0].upper()      
        txt["cat"] = text[ri][1]      
        txt["cur"] = podkr( txt["text"]  )   
        c.execute("INSERT OR IGNORE INTO config(conf,serwer, id) VALUES (?,?,'kolo_text');", (json.dumps(txt) ,idsrv,))   
        conn.commit()       
        await utils.upload_sett()  
    if params[0] =="" : return #wyślij zasady
    
    #if params[0].lower() == "kup" : #kup litere
    #    print("kup litere")
    #    return
        
    #if params[0].lower() == "rank" : #ranking
     #   print("ranking")
     #   return
    ll = False
    if len(params[0])==1 : #strzel litere
        l = params[0].upper()
        if l in txt["text"] and not l in txt["cur"]:
            txt["cur"] = litera(txt, l)
            c.execute("UPDATE OR IGNORE config SET conf=? WHERE id='kolo_text' AND serwer=?;", (json.dumps(txt) ,idsrv,))   
            conn.commit()       
            ll = True if txt["cur"] == txt["text"] else  False
        else: 
            pass
    
    embed = discord.Embed(color=0xFFFF00)
    if len(message.content)>1 or ll: #odgadnij haslo
        if message.content.upper() == txt["text"] or ll:
            embed.title = "Gratulacje!"            
            embed.description = "Hasło `{}` odgaduje: {} i zdobywa: {}pkt.\n\nAby rozpocząć nową rundę - podaj literę.".format(txt["text"], message.author.mention, "<do obmyślenia>" )
            
            c.execute("DELETE FROM config WHERE id='kolo_text' AND serwer=?;", (idsrv,)) 
            conn.commit()    
            await message.channel.send(embed=embed) 
            return
        else:
            embed.description = "{} To błędne hasło - tracisz **{}**pkt".format(message.author.mention, "<do obmyślenia>" )
       
            await message.channel.send(embed=embed) 
            
    #print(txt)
    
    embed.title = "Kto odgadnie hasło?"
    cat = " - "+txt["cat"] if txt["cat"] else ""
    embed.description = "`{}`".format(txt["cur"]) + cat
    await message.channel.send(embed=embed) 
    
    
    
async def tenor(txt):
    t = TenGiphPy.Tenor(token='77LXLCAA979K')
    return t.random(txt)       
        
            
async def tgif(txt):
    g = re.findall(r'(?i){gif:[a-z0-9 \-\_ąęśćżźńół]+}',txt )
    if g: return await tenor(g[0].replace("{gif:","").replace("}","") )
    return txt


async def gimg(txt):
    r = requests.get('https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +                SEARCH_ENGINE_ID + '&q=' + txt + '&searchType=image',headers={'referer': 'https://heroku.com'}, allow_redirects=True)
    data = r.content.decode('utf-8')   
        
    data = json.loads(data)
    link = []
    if 'items' in data:
        for j in data['items']:
            link.append(j['link'])
    else: return 
    return random.choice(link)
    
async def timg(txt):
    g = re.findall(r'(?i){img:[a-z0-9 \-\_ąęśćżźńół]+}',txt )
    if g: return await gimg(g[0].replace("{img:","").replace("}","") )
    return txt

    
async def censore(message, client):
    id = str(message.guild.id)
    for k in c.execute("SELECT conf FROM config WHERE serwer=? and id='log';", (id,)):
        if int(k[0])==message.channel.id: return
    cnf=[]
    for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='censore';", (id,)):
        if j: cnf = json.loads(j[0])   

    for i in cnf:
        m = message.content.replace("​","")
        m = m.replace("*","")
        #if len(re.findall(r'{}'.format(i) ,message.content))>0:
        s = re.search(r'{}'.format(i),message.content)
        if s:
            msg = await message.channel.send( "{} Nie używamy tutaj takiego słownictwa.".format(message.author.mention))
            try:
                await message.delete()
                await msg.delete(delay=1)  
                embed = discord.Embed(color=0x00ff00)
                embed.title = "Filtr słów"
                msg = message.content.replace("__","")
                msg = msg.replace(s[0],"__"+s[0]+"__")
                embed.description = "Filtr: `{}`\n\nTreść: \n{}".format(i,msg)
                embed.set_footer(text ="#{} → {}".format( message.channel.name, message.author))
                await utils.log(id,"",client, embed)           
            except :
                pass   
            return
    
    
    return


async def scc(message, client):
    id = str(message.guild.id)
    cmd = message.content[len(settings.COMMAND_PREFIX):].strip()
    i = cmd.split(' ')
    if len(i)>0 : 
        cmd = i[0].strip().lower()
    else: 
        return
    
    scmd = i[1].strip().lower() if len(i)>1 else ""
        
    gc = await utils.gc(id, cmd, client)
    j={}
    cnf={}
    for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=?;", (id,"scmd_"+cmd) ):
        if j: cnf=json.loads(j[0])        
        
    if not cnf: return    
    try: await message.delete()
    except : pass    
            
    sc=[]
    for l in cnf["subcmd"].keys():
        sc.append(l)

    oscmd = scmd    
    chars = ["<",">","!","@","#"]
    for d in chars:
        scmd = scmd.replace(d,"")

    if not oscmd == scmd:
        for l in sc:
            if l == oscmd:
                cnf["subcmd"][scmd]  = cnf["subcmd"][oscmd]
                cnf["subcmd"].pop(oscmd)
        
    if scmd=="" or not scmd in cnf["subcmd"]:    
        msg="Dla komendy `{}` istnieją następujące sub-komendy: `{}`".format(cmd, ", ".join(sc))
        if gc: await gc.send(msg)
        else: await message.channel.send(msg)
        if not client.user.id == message.author.id: 
            await utils.stat(cmd=cmd, srv=message.guild.id, local =1) #stats
        return

    
    odp2=[]
    for k in cnf["subcmd"][scmd]:
        odp2.append(cnf["subcmd"][scmd][k])        
    
            
    odp = odp2[randint(0, len(odp2)-1)] 

    
    usrav=[]
    usrni=[]
    
    if (message.mentions.__len__()>0):
            for user in message.mentions:
                usrav.append(str(user.avatar_url_as(static_format ="jpg",size =1024)))
                usrni.append(user.nick if user.nick else user.name)
    try:               
        nick = message.author.nick if message.author.nick else message.author.name
    except:
        nick = message.author.display_name
    av = str(message.author.avatar_url_as(static_format ="jpg",size =1024))

    rest = message.content[len(settings.COMMAND_PREFIX)+len(cmd):].strip()
    rest = rest[len(scmd):].strip()

    odp["odp"] = odp["odp"].replace("{autor.nick}", nick)  
    odp["tyt"] = odp["tyt"].replace("{autor.nick}", nick) 
    odp["img"] = odp["img"].replace("{autor.avatar}", av )
    odp["th"] = odp["th"].replace("{autor.avatar}", av )
    
    odp["img"] = odp["img"].replace("{param.avatar}", usrav[0] if usrav else "")
    odp["th"] = odp["th"].replace("{param.avatar}", usrav[0] if usrav else "")
    odp["odp"] = odp["odp"].replace("{param.nick}", usrni[0] if usrni else "")  
    odp["tyt"] = odp["tyt"].replace("{param.nick}", usrni[0] if usrni else "")
    
    
    odp["odp"] = odp["odp"].replace("{autor}", message.author.mention)
    odp["odp"] = odp["odp"].replace("{param}", rest)
    odp["tyt"] = odp["tyt"].replace("{param}", rest)
    
    odp["img"] = await tgif(odp["img"])  
    odp["th"] = await tgif(odp["th"])  
    
    odp["img"] = await timg(odp["img"])  
    odp["th"] = await timg(odp["th"])  
        





    embed = discord.Embed(color=0x00ff00)
    embed.title = odp["tyt"]
    embed.description = odp["odp"]
    if odp["img"] : embed.set_image (url=odp["img"])
    if odp["th"]  : embed.set_thumbnail (url=odp["th"])
    if gc: await gc.send(embed=embed)
    else: await message.channel.send(embed=embed)        
    if not client.user.id == message.author.id: 
        await utils.stat(cmd=cmd, srv=message.guild.id, local =1) #stats


    return
    
    
    
    
    
async def custom_command(message, client):
    if message.content[0:len(settings.COMMAND_PREFIX)] !=settings.COMMAND_PREFIX: return
    print(message.content)
    id = str(message.guild.id)
    cmd = message.content[len(settings.COMMAND_PREFIX):].strip()
    i = cmd.split(' ', 1)
    if i : cmd = i[0].strip().lower()
    rest = message.content[len(settings.COMMAND_PREFIX)+len(cmd):].strip()
    odp=[]
    for i in c.execute("SELECT txt FROM command WHERE srv=? AND cmd=?;", (id,cmd) ):
        if i: odp.append(i[0])
    


##########################################
    cnf = {}
    cmd = message.content[len(settings.COMMAND_PREFIX):].strip()
    i = cmd.split(' ', 1)
    if i : cmd = i[0].strip().lower()
    odp2=[]
    for j in c.execute("SELECT conf FROM config WHERE serwer=? AND id=?;", (id,"cmd_"+cmd) ):
        if j: cnf=json.loads(j[0])
        
    for i in cnf:
        if i: odp2.append(cnf[i])
  
    if not odp and not odp2: return    
    try:
        await message.delete()
    except :
        pass
        
    v = 0
    if odp and odp2: v =  randint(0,1)
    if not odp and odp2: v = 1
    usrav=[]
    usrni=[]
    
    if (message.mentions.__len__()>0):
            for user in message.mentions:
                usrav.append(str(user.avatar_url_as(static_format ="jpg",size =1024)))
                usrni.append(user.nick if user.nick else user.name)
                
    try:               
        nick = message.author.nick if message.author.nick else message.author.name
    except:
        nick = message.author.display_name
        
    av = str(message.author.avatar_url_as(static_format ="jpg",size =1024))
    
    
    if v == 1:    
        odp2 = odp2[randint(1, len(odp2)-1)]  
        
        odp2["odp"] = odp2["odp"].replace("{autor.nick}", nick)  
        odp2["tyt"] = odp2["tyt"].replace("{autor.nick}", nick) 
        odp2["img"] = odp2["img"].replace("{autor.avatar}", av )
        odp2["th"] = odp2["th"].replace("{autor.avatar}", av )
        
        odp2["img"] = odp2["img"].replace("{param.avatar}", usrav[0] if usrav else "")
        odp2["th"] = odp2["th"].replace("{param.avatar}", usrav[0] if usrav else "")
        odp2["odp"] = odp2["odp"].replace("{param.nick}", usrni[0] if usrni else "")  
        odp2["tyt"] = odp2["tyt"].replace("{param.nick}", usrni[0] if usrni else "")
        
        
        odp2["odp"] = odp2["odp"].replace("{autor}", message.author.mention)
        odp2["odp"] = odp2["odp"].replace("{param}", rest)
        odp2["tyt"] = odp2["tyt"].replace("{param}", rest)
        
        odp2["img"] = await tgif(odp2["img"])  
        odp2["th"] = await tgif(odp2["th"])  
        
        odp2["img"] = await timg(odp2["img"])  
        odp2["th"] = await timg(odp2["th"])  
        
        
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = odp2["tyt"]
        embed.description = odp2["odp"]
        if odp2["img"] : embed.set_image (url=odp2["img"])
        if odp2["th"]  : embed.set_thumbnail (url=odp2["th"])
        gc = await utils.gc(id, cmd, client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        if not client.user.id == message.author.id: 
            await utils.stat(cmd=cmd, srv=message.guild.id, local =1) #stats
        return
        
        
    #print(randint(0, len(odp)-1))
    odp = odp[randint(0, len(odp)-1)]
    odp = odp.replace("{autor.nick}", nick)  
    odp = odp.replace("{autor}", message.author.mention)
    odp = odp.replace("{param}", rest)
    gc = await utils.gc(id, cmd, client)
    if gc: await gc.send(odp)
    else: await message.channel.send(odp)
    
     
###############################################################################
async def licz(message):
    id = str(message.guild.id)
    cid = str(message.channel.id)
    maxx = 10000
    proc = 25 # % dopisku
    proc2 = 50 # % kolejnej liczby
    for i in c.execute("SELECT conf FROM config WHERE serwer=? AND id='licz' LIMIT 1;", (id,) ):
        if i[0]!=cid: break
        for z in c.execute("SELECT conf FROM config WHERE serwer=? AND id='licz_max' LIMIT 1;", (id,) ):
            if z: maxx = z[0]
        for z in c.execute("SELECT conf FROM config WHERE serwer=? AND id='licz_proc' LIMIT 1;", (id,) ):
            if z: proc = float(z[0])
        for z in c.execute("SELECT conf FROM config WHERE serwer=? AND id='licz_odp' LIMIT 1;", (id,) ):
            if z: proc2 = float(z[0])
        l=10
        j=k=n=0
        lm=""
        o = True
        messages = await message.channel.history(limit=l, oldest_first=True, around =message).flatten()
        for m in messages:
            i = re.findall(r'\d+',m.content.replace("​",""))
            if not i: 
                try: await m.delete()
                except expected_exc: pass
                o = False
                continue
            i=int(i[0])
            if k==0: k=i
            if i-j == k: 
                j+=1
                n=i
                lm = m.author.mention
            else:     
                o = False
                try: await m.delete()
                except expected_exc: pass
        
        if lm == "": return
        if re.findall(r'\d+',lm)[0]  == bot_id: return
        if randint(0,100)>=100-proc2 and k and o: 
            msg=""
            if randint(0,100)>=100-proc: 
                odp=[]
                for i in c.execute("SELECT odp FROM licz;" ):
                    if i[0]: odp.append(i[0])
                r = randint(0, len(odp)-1) 
                msg = await utils.fformat(odp[r], n+1, int(maxx)  )          
            await message.channel.send(str(n+1) + " " +msg)
            #await message.reply(str(n+1) + " " +msg, mention_author=False)
###############################################################################
async def slowmode(message, client):
    slow = settings.SLOW
    uid = str(message.author.id)
    sid = str(message.guild.id)
    if not sid in slow: return
    if uid in slow[sid]:
        t3 = int(message.created_at.timestamp())
        t4 = int(slow[sid][uid]["l"]) + int(slow[sid][uid]["s"])
        slow[sid][uid]["l"] = t3
        if t4 > t3 or len(message.content)>int(slow[sid][uid]["z"]):
            msg = await message.channel.send(message.author.mention + " Nałożono na Ciebie ograniczenia! Możesz wysyłać wiadomość raz na {} sekund z limitem {} znaków!".format(slow[sid][uid]["s"], slow[sid][uid]["z"]) )
            await message.delete()
            await msg.delete(delay=10)  
    return
    
async def sl():
    for i in c.execute("SELECT conf FROM config WHERE id=?;", ("slowmode",) ):
        if i : 
            settings.SLOW = json.loads(i[0])
            break




async def msgdb(message):  
    con = settings.conn
    c = settings.c
    id = message.guild.id

    attach=[]
    embed=[]
    for a in message.attachments:
        attach.append(a.url)                    
    attach=json.dumps(attach )
    for a in message.embeds:
        embed.append(a.to_dict())                    
    embed=json.dumps(embed )

    c.execute("INSERT OR IGNORE INTO msg('msg','chan','autor','idmsg','srv','time', 'edit', 'attach', 'embed') SELECT ?,?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT x FROM msg WHERE srv=? AND idmsg=? AND chan=?);", (message.content, message.channel.id, message.author.id , message.id, id, message.created_at,message.edited_at, attach, embed,          id,  message.id, message.channel.id))
    #c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( cnf, cnfid, id))
    conn.commit()




async def msgdbedit(message, client):    # po edycji 
    con = settings.conn
    c = settings.c
    id = message.guild_id

    attach=[]
    embed=[]
    try:
        for a in message.data["attachments"]:
            attach.append(a.url)                    
        attach=json.dumps(attach )
    except:pass
    try:
        for a in message.data["embeds"]:
            embed.append(a.to_dict())                    
        embed=json.dumps(embed )
    except:pass    
    k = True
    for j in c.execute("SELECT x FROM msg WHERE srv=? AND idmsg=? AND chan=?;", (id, message.message_id, message.channel_id)):
        if j[0]: k = False
    if k: 
        channel = client.get_channel(message.channel_id)
        m = await channel.fetch_message(message.message_id)
        print(m)
        await msgdb(m)
        return
    
    
    hst = []
    for j in c.execute("SELECT history FROM msg WHERE srv=? AND idmsg=? AND chan=? LIMIT 1;", (id, message.message_id, message.channel_id) ):
        hst = json.loads(j[0]) if j[0] else []
    
    try: m= message.data["content"] 
    except:pass    
    aft = {"msg":m, "embed":embed, "attach":attach, "data":str(message.data["edited_timestamp"])}
    hst.append(aft)
    #print(hst)
    hst = json.dumps(hst)
    
    c.execute("UPDATE OR IGNORE msg SET history=?, edit=? WHERE srv=? AND idmsg=? AND chan=?;", (hst,str(message.data["edited_timestamp"]), id,message.message_id, message.channel_id  ))
    conn.commit()




    from discord.ext import commands



def main():
    # Initialize the client
    print("Starting up...")
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True	
    intents.message_content = True
    client = discord.Client(intents=intents)
    #client = discord.Client(intents=discord.Intents.all())
    #slash = SlashCommand(client, sync_commands=True)
    

    #client = commands.Bot(command_prefix="!")
    #client = discord.Bot()


    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag
    @client.event
    async def on_ready():
        if this.running:
            return
        this.running = True
        await sl()
        await utils.import_sett() ########################
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (client,),
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)
    # The message handler for both new message and edits

    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            if len(cmd_split)<2: cmd_split.append("")
            try:
                await message_handler.handle_command(cmd_split[0].lower(),
                                      cmd_split[1:], message, client)
            except:
                print("Error while handling message", flush=True)
                raise

    @client.event
    async def on_message(message):        
        await msgdb(message)
        if message: await slowmode(message,client) 
        if message: await censore(message,client) 
        if message: await custom_command(message, client)
        if message: await scc(message, client)
        if message: await common_handle_message(message)
        if message: await licz(message)
        if message: await kolo(message, client)
        
    @client.event
    async def on_raw_message_edit(p):
       # print(p)
        #await msgdbedit(p,client)
        pass
        

    @client.event
    async def on_message_edit(before, after):
        if after: await censore(after,client)
        if after: await custom_command(after, client)
        if after: await scc(after, client)
        if after: await common_handle_message(after)

    @client.event
    async def on_member_update(before, after):
        return
        pprint(after.roles)
        channel = client.get_channel(518828594173181986) #testy
        i=0;
        for r in after.roles:
            if r.name == "green": i+=1

        for r in before.roles:
            if r.name == "green": i=0
        if i>0: await channel.send( before.mention+ "  Witaj przybyszu z odległych serwerów!")

    @client.event
    async def on_message_delete(message):
        print(message.author.name, message.content)
        
        
    #@slash.slash(name="ruda", description="Moja lista komend.")
    #async def ruda(ctx):
     # await ctx.send(content="!ruda")    

  
    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)

###############################################################################


if __name__ == "__main__":
    main()
