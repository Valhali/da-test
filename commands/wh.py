from commands.base_command  import BaseCommand
import requests
import re, os, settings
import utils, discord, time
from discord.ext import commands

class Wh(BaseCommand): 

    def __init__(self):
        description = ""
        params = [""]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:            await message.delete()
        except :        pass
        


        webhook = await message.channel.create_webhook(name=message.author.display_name)
        await webhook.send(
            message.content[4:], username=message.author.display_name, avatar_url=message.author.avatar_url)
        try:
            webhooks = await message.channel.webhooks()
            for webhook in webhooks:
                    await webhook.delete()
        except:pass
        