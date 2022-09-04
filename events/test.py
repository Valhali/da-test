from events.base_event      import BaseEvent
from utils                  import get_channel
import settings
from datetime               import datetime

class Dzis(BaseEvent):

    def __init__(self):
        interval_minutes = 1  # Set the interval for this event
        super().__init__(interval_minutes)

    async def run(self, client):
        #print(settings.SETTINGS)
        pass
        #channel = get_channel(client, f"testy")
        #await client.send_message(channel, msg)
