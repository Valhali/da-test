from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import re

class Del(BaseCommand):

    def __init__(self):
        description = ""
        params = ["ilość"]
        super().__init__(description, params)

    async def handle(self, params, message, client):

        if re.findall(r'\d+',message.author.mention)[0]  == "188721035133059072" or message.author.guild_permissions.kick_members:
            messages = await message.channel.history(limit=int(params[0])).flatten()
            for m in messages:
                await m.delete()
