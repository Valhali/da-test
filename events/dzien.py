from events.base_event      import BaseEvent
from utils                  import get_channel
import settings
from datetime               import datetime


class Dzis(BaseEvent):

    def __init__(self):
        interval_minutes = 1  # Set the interval for this event
        super().__init__(interval_minutes)

    async def run(self, client):
        now = datetime.now()
        msg = settings.COMMAND_PREFIX + "dzien"

        cn = [776866188247564299]
        if now.hour == 4 and now.minute == 30 :
            for ch in cn:
                channel = client.get_channel(ch)
                await channel.send(msg)


        cn = [776866188247564299]
        if now.hour == 18 and now.minute == 37:
            for ch in cn:
                channel = client.get_channel(ch)
                await channel.send(settings.COMMAND_PREFIX +"pogoda jaworzno ")
                t = datetime.now()
                y=str(t.year)
                m=str(t.month)
                d=str(t.day)
                await channel.send("<@188721035133059072> https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate="+y+m+d+"12&row=462&col=220&lang=pl")
        #channel = get_channel(client, f"testy")
        #await client.send_message(channel, msg)
