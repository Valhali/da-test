from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json, os
from PIL import Image, ImageDraw, ImageFont
import settings, io, discord,aiohttp, utils
from datetime import datetime

class _Img(BaseCommand):

    def __init__(self):
        description = ""
        params = ["miasto"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        fontsFolder = 'C:\Windows\Fonts'
        arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 16)
        msg = ""
        im= Image.new("RGBA", (128, 128))
        draw = ImageDraw.Draw(im)
        draw.text((10, 10), 'ONEIRO', fill='red', font=arialFont)
        #im.show()
        
        #############################################################
        with io.BytesIO() as image_binary:
            im.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(image_binary, "img.jpg")
        #await message.channel.send(msg, file=file)
        ##############################################################
        my_url="https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0131.jpg"
        file = await utils.dimg(my_url)
        await message.channel.send(msg, file=file)