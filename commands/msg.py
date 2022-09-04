from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import re, settings

conn = settings.conn
c = settings.c
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Msg(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        id = str(message.guild.id)
        cid = str(message.channel.id)
        for i in c.execute("SELECT conf FROM config WHERE serwer=? AND id='licz' LIMIT 1;", (id,) ):
            if i[0]==cid: return
        try:
            await message.delete()
        except :
            pass
        
        msg = ' '.join([str(elem) for elem in params])

        if re.findall(r'\d+',message.author.mention)[0]  == "188721035133059072" or message.author.guild_permissions.kick_members:
            await message.channel.send(msg)
