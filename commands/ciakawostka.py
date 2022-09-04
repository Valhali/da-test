from commands.base_command  import BaseCommand
import urllib.request, json, discord, utils
from random                 import randint

class Ciekawostka(BaseCommand):

    def __init__(self):
        description = "Ciekawostka z różcnych dziedzin"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        with urllib.request.urlopen("https://do-liczyk.sourceforge.io/bocinka/?c") as url:
            data = json.loads(url.read().decode())

        str1 = ""

        m = len(data["ciekawostki"])-1
        i = randint(0, m)

        str1 +=data["ciekawostki"][i]



        #msg = f"```" + str1 +f"```"
        #await message.channel.send(msg)
        
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Ciekawostka ({:d}/{:d})".format(i+1, m+1 )
        embed.description = str1
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "ciekawostka", client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)


