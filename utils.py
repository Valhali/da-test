from os.path    import join
from os         import remove

from discord    import HTTPException
from emoji      import emojize
import emoji

import urllib.parse
import requests, aiohttp, io, discord
import settings
import sqlite3, json,zlib
from datetime import datetime
from datetime import *
from dateutil.tz import *
from dateutil import tz
from bs4 import BeautifulSoup


# Returns a path relative to the bot directory
def get_rel_path(rel_path):
    return join(settings.BASE_DIR, rel_path)


# Returns an emoji as required to send it in a message
# You can pass the emoji name with or without colons
# If fail_silently is True, it will not raise an exception
# if the emoji is not found, it will return the input instead
def get_emoji(emoji_name, fail_silently=False):
    alias = emoji_name if emoji_name[0] == emoji_name[-1] == ":" \
            else f":{emoji_name}:"
    the_emoji = emojize(alias, use_aliases=True)

    if the_emoji == alias and not fail_silently:
        raise ValueError(f"Emoji {alias} not found!")

    return the_emoji


# A shortcut to get a channel by a certain attribute
# Uses the channel name by default
# If many matching channels are found, returns the first one
def get_channel(client, value, attribute="name"):
    channel = next((c for c in client.get_all_channels()
                    if getattr(c, attribute).lower() == value.lower()), None)
    if not channel:
        raise ValueError("No such channel")
    return channel


# Shortcut method to send a message in a channel with a certain name
# You can pass more positional arguments to send_message
# Uses get_channel, so you should be sure that the bot has access to only
# one channel with such name
async def send_in_channel(client, channel_name, *args):
    await client.send_message(get_channel(client, channel_name), *args)


# Attempts to upload a file in a certain channel
# content refers to the additional text that can be sent alongside the file
# delete_after_send can be set to True to delete the file afterwards
async def try_upload_file(client, channel, file_path, content=None,
                          delete_after_send=False, retries=3):
    used_retries = 0
    sent_msg = None

    while not sent_msg and used_retries < retries:
        try:
            sent_msg = await client.send_file(channel, file_path,
                                              content=content)
        except HTTPException:
            used_retries += 1

    if delete_after_send:
        remove(file_path)

    if not sent_msg:
        await client.send_message(channel,
                                 "Oops, something happened. Please try again.")

    return sent_msg



async def upload_sett(): #########################
    return
    l="" 
    a=[]
    b=[]
    js={}
    con = settings.conn
    c = settings.c
    con.commit()    
    r = c.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    rows = c.fetchmany(1000)
    for r in rows:
        if r[0] =="moon": continue
        #if r[0] =="msg": continue 
        rows2 = c.execute("SELECT * FROM {:s}".format(r[0]))
        a=[]
        b=[]
        for r2 in rows2:
            a.append(r2)
       # print(r[0])
        rows2 = c.execute("PRAGMA table_info({:s})  ".format(r[0]))
        for r2 in rows2:
            #print("r2\t",r2)
            b.append(r2[1])
        
        js[r[0]]=[r[1], b, a]
    l = json.dumps(js)
    
        
    #return
    
    l = zlib.compress(l.encode())
    #s = requests.post("https://darkorbitfaq.sourceforge.io/ruda/bsql/upd.php", data={'x': l, 'type': 'issue', 'action': 'show'})
    s = requests.post("http://localhost/bocinka/bsql/upd.php", data={'x': l, 'type': 'issue', 'action': 'show'})
    #s = requests.post("http://oneiro.epizy.com/ruda/bsql/upd.php", data={'x': l, 'type': 'issue', 'action': 'show'})
    print("{:.2f}".format(len(l )/1024.0),"kb → \n", s.status_code, s.reason, s.content.decode('utf-8'))
    con.commit()    
        
      ############################################  

async def _upload_sett():
    return
    l=""
    con = settings.conn
    for line in con.iterdump():
        l+=line+"\n"
            
    #s = requests.post("https://do-liczyk.sourceforge.io/bocinka/?s=RUDA_SETTINGS", data={'set': l, 'type': 'issue', 'action': 'show'})
    print("{:.2f}".format(len(l )/1024.0),"kb → \n", s.status_code, s.reason, s.content.decode('utf-8'))
    con.commit()    
        

async def import_sett():
    return
    l=""
    con = settings.conn
    c = settings.c
    t = str(datetime.now()        )
    s = requests.get("http://localhost/bocinka/bsql/upd.php?i&t="+t, allow_redirects=True)
    #s = requests.get("https://darkorbitfaq.sourceforge.io/ruda/bsql/upd.php?i&t="+t, allow_redirects=True)
    #s = zlib.decompress(s.content).decode('utf-8')
    s = s.content.decode('utf-8')
    js = json.loads(s)
    for i in js:
        k = []
        for j in range(0,len(js[i][0])):
            k.append("?")
        col = ",".join(k)
        if js[i][1]: c.execute("DELETE FROM {:s}".format(i))        
        for l in js[i][1]:
            c.execute("INSERT OR IGNORE INTO {:s} VALUES ({:s})".format(i, col),l)
            #print(l)
        
    con.commit()
                
        

        

async def fformat(odp, v,m=10000):
    odp = odp.replace("{proc}", "{:.2f}".format(v/m*100 ) )
    return odp
    
    


    
async def dimg(url, name="img.png"):
    async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as resp:
                if resp.status != 200:
                    return 
                data = io.BytesIO(await resp.read())
                file = discord.File(data, name)
                return file
    


async def log(id, msg="",client=0,em=""):  
    con = settings.conn
    c = settings.c
    for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='log';", (id,)):
        pass
     
    channel = client.get_channel(int(j[0]) )
    if channel: 
        if em: await channel.send(embed=em)
        if msg: await channel.send(msg)
        
        
        

async def gc(id,cmd,client): 
    con = settings.conn
    c = settings.c
    js={}
    for j in c.execute("SELECT conf FROM config WHERE serwer=? and id='response';", (id,)):
        if j: js = json.loads(j[0])   
    if not js: return None
    iid = 0
    if cmd in js["cmd"].keys(): 
        iid = js["cmd"][cmd]
    else:
        iid = js["def"]
        
        
    channel = client.get_channel(int(iid) )
    if channel: return channel
    return None
    
    
async def send(*, client, message, cmd="", msg="", embed=None, file=None)  : 
    ch = None
    if not client.user.id == message.author.id: 
        ch = await gc(message.guild.id, cmd, client)
    if ch: return await ch.send(content =msg, embed=embed,file= file )
    else: return await message.channel.send(content =msg, embed=embed,file= file)
    
    
    
       
    

async def stat(*, cmd="", srv=0, local=0):
    stats={}
    conn = settings.conn
    c = settings.c
    for i in c.execute("SELECT conf FROM config WHERE id=? AND serwer=?;", ("stats",0) ):
        if i : 
            stats = json.loads(i[0])
            break
    if not cmd in stats:    stats[cmd] = 1
    else: stats[cmd] +=1
    
    if stats and not local: 
        s = json.dumps(stats)
        await stat_upd(0, s)
        c.execute("INSERT OR IGNORE INTO config(conf, id, serwer) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? and serwer=? );", (s, "stats", 0 , "stats", 0)) 
        c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? and serwer=?;", ( s, "stats",0)) 
           
    
    ######################################    
    stats={} #local 
    conn = settings.conn
    c = settings.c
    for i in c.execute("SELECT conf FROM config WHERE id=? AND serwer=?;", ("stats",srv) ):
        if i : 
            stats = json.loads(i[0])
            break
    if not cmd in stats:    stats[cmd] = 1
    else: stats[cmd] +=1
    
    if stats:
        s = json.dumps(stats)
        await stat_upd(srv, s)
        c.execute("INSERT OR IGNORE INTO config(conf, id, serwer) SELECT ?,?,? WHERE NOT EXISTS (SELECT x FROM config WHERE id=? AND serwer=?);", (s, "stats" ,srv, "stats", srv)) 
        c.execute("UPDATE OR IGNORE config SET conf=? WHERE id=? AND serwer=?;", ( s, "stats", srv)) 
    
    conn.commit()
    
    
async def stat_upd(srv="", stat=""):

    con = settings.conn
    c = settings.c
    #s = requests.post("https://darkorbitfaq.sourceforge.io/ruda/bsql/upd.php", data={'s': stat, 'srv': srv, 'action': 'show'})
    s = requests.post("http://localhost/bocinka/bsql/upd.php", data={'s': stat, 'srv': srv, 'action': 'show'})
    print(s.content.decode('utf-8'))
    con.commit()    
            
            
            
            
async def calend_update():
    print("update")
    conn = settings.conn
    c = settings.c
        
    mies = ["0",        
            ["Styczeń","stycznia"],        
            ["Luty", "lutego"],        
            ["Marzec","marca"],        
            ["Kwiecień","kwietnia"],        
            ["Maj","maja"],
            ["Czerwiec", "czerwca"],
            ["Lipiec","lipca"],        
            ["Sierpień","sierpnia"],        
            ["Wrzesień","września"],        
            ["Październik","października"],
            ["Listopad","listopada"],        
            ["Grudzień","grudnia"]
            ]
            
            
    dn =        datetime.now(tzutc())
    ye = datetime(dn.year, 12, 31)    
    ye = int( ye.strftime("%j"))+1
    print(ye)
    
    msg={}

    r = requests.get("http://nonsa.pl/wiki/Kalendarz_%C5%9Bwi%C4%85t_nietypowych", allow_redirects=True)
    soup = BeautifulSoup(r.content, 'html.parser')
    m3=0
    for i in range(1, ye):        
        d1 = datetime.strptime(str(i), "%j").replace(year= dn.year)
        m1 = int(d1.strftime("%m") )
        d = int( d1.strftime("%d"))
        przyslowie=[]
       
                
        if not m1 == m3:           
            r3 = requests.get("https://www.kalbi.pl/przyslowia-polskie-na-{}".format(mies[m1][0].replace("ś","s").replace("ź","z").replace("ń","n").lower()), allow_redirects=True)
            
            #.encode('utf-8')
            s = r3.content.decode().replace("<br />","|")
            soup3 = BeautifulSoup( s, 'html.parser')
            results0 = soup3.find( class_='calProverb_m').find( "tbody").findAll("tr")
            m3=m1
            
            
        for i in results0[d-1].findAll("td")[1].text.split("|")  :
            przyslowie.append(i)
        
        
        mt=[]
        if not str(m1) in msg: msg[str(m1)]={}        
        if not str(d) in msg[str(m1)] : msg[str(m1)][str(d)]={}   

        
        ###############################
        r2 = requests.get("http://www.kalbi.pl/{}-{}".format(d,mies[m1][1].replace("ś","s").replace("ź","z")), allow_redirects=True)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        try: 
            results = soup2.find( class_='calCard-ententa').findAll( "a")
            m2 = soup2.find( class_='calCard-fete')
            m2 = m2.findAll( "a") if m2 else ""
            dzis="{} {:s}".format(d, mies[m1][0])
            if m2:
                for m in m2:
                    if m.text.lower() and not m.text.strip().lower() in map(str.lower ,mt): 
                        mt.append(m.text.strip())
            for m in results:
                if m.text.lower() and not m.text.strip().lower() in map(str.lower ,mt): 
                    mt.append(m.text.strip())
        except:pass    
        
                       
        
        #if results : przyslowie = results.text.replace("„",'"').replace("”",'"|').split("|")        
        przyslowie =  json.dumps(przyslowie) if przyslowie else "{}"
        
        results = soup2.find( class_='calCard-quotes').find( class_='calCard_proverb-content')
        if results : cytat = results.text.replace("„","").replace("”","").strip()
        
        imieniny=[]
        results = soup2.find( class_='calCard-name-day').findAll( "a")
        for m in results:
            if m : imieniny.append(m.text.strip())
        imieniny = json.dumps(imieniny)
        
        results = soup2.find( class_='calCard-quotes').find( class_='calCard_proverb-content')
        cytat = results.text.replace("„","").replace("”","").strip() if results else ""
        
        soup2=None    
        
        ###############################

        
        #try:    
        dzis = "{} {}".format(d, mies[m1][1])    
        results = soup.find("a", title=dzis).parent.text
        msg1 = []
        results = results.replace(dzis+" – ","").split(", ")
        for m in results:
            if m.lower() and not m.strip().lower() in map(str.lower ,mt):  
                mt.append( m.strip() )
        #except:pass        
            
        #print(d, m1, mt, "\n\n")    
            
        c.execute("INSERT OR IGNORE INTO calendar (day, month, swieto,przyslowie,imieniny, cytat) VALUES (?,?,?,?,?,?);", (d,m1,json.dumps(mt,indent=4), przyslowie,imieniny, cytat ))
    conn.commit() 
    return

            
            
            
async def emojiavail(guild, emote):
    try:
        emote_name = emote.split(':')[1]
        for emote in guild.emojis:
            if emote.name == emote_name:
                return emote          
    except: emote_name = emote
    
    if emoji.emoji_count(emote_name) > 0:
        return emote

    return None

    