from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json
#from PIL import Image, ImageDraw, ImageFont
import settings
from datetime import datetime
import windyLib

class Windy(BaseCommand):

    def __init__(self):
        description = "Pogoda"
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        a = windyLib.windyWeather('ec', 19.67, 52.86)
        a = windyWeather('ec', 19.67, 52.86)
        print(a.getInfo())
        print(a.getCertainTimeVerticalWeather(0))

