from events.base_event      import BaseEvent
from utils                  import get_channel
import settings
from datetime               import datetime
import json, discord
from mee6_py_api import API

class Mee6(BaseEvent):

    def __init__(self):
        interval_minutes = 30  # Set the interval for this event
        super().__init__(interval_minutes)

    async def run(self, client):
        now = datetime.now()
                       
        channel = client.get_channel(603311200905986048)
        
        mee6API = API(518828593741299717)
        i = 0
        while 1: 
            leaderboard_page = await mee6API.levels.get_leaderboard_page(i)
            i+=1
            if not leaderboard_page["players"]: break
            for j in leaderboard_page["players"]:
                if j["level"]>=10:
                    k = channel.guild.get_member(int(j["id"]))
                    print(type(k), k)
                    if not k: continue
                    if isinstance(k,discord.member.Member): 
                        role = discord.utils.get(k.guild.roles, name="Śpioch")
                        if role not in k.roles:
                            await k.add_roles(role )
        