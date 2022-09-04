from commands.base_command  import BaseCommand
import requests
import json
import settings
import re, os, zlib
from datetime import datetime
import utils 

class Db(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        conn = settings.conn
        c = settings.c
        skip = 0
        #print(params)
        #return
        if params : skip =1 if params[0]=="1" else 0
        text_channel_list = []
        if skip==0:
            servers = client.guilds
            for s in servers:
                print(s.id, " → ", s.name)
                for ch in s.text_channels:
                    text_channel_list.append(ch) 
                    print ("\t",ch.id, " → ", ch.name)
                    
                    try:
                        messages = await ch.history(limit=1000000, oldest_first=True).flatten()
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
                        
                        c.execute("INSERT OR IGNORE INTO msg (msg, chan, autor,idmsg,idchan,idsrv,idautor,time,edit,attach,embed) VALUES (?,?,?,?,?,?,?,?,?,?,?);", (m.content,ch.name, m.author.name, m.id,ch.id,s.id,m.author.id, m.created_at,m.edited_at, attach, embed))
                        c.execute("UPDATE OR IGNORE msg SET autor=?, msg=? WHERE idmsg=?;",     ( m.author.name,m.content, m.id))
                    conn.commit()  
       
        #conn.commit()    
        await utils.upload_sett()  
        #return