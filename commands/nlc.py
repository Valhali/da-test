from commands.base_command  import BaseCommand
import urllib.request, json
import base64
import discord
import re
import requests, io, discord, utils


class Nlc(BaseCommand):

    def __init__(self):
        description = "Obłoki srebrzyste"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        msg = ""
        url= "http://www.iap-kborn.de/fileadmin/user_upload/MAIN-abteilung/radar/Radars/OswinVHF/Plots/OSWIN_Mesosphere_4hour.png"


        f = await utils.dimg(url,"os.png")
        embed = discord.Embed(color=0x55ff00)
        embed.title = "Obłoki srebrzyste"
        
        embed.set_image(url="attachment://os.png")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ob%C5%82oki_srebrzyste_nad_Tarnowskimi_G%C3%B3rami.jpg/1024px-Ob%C5%82oki_srebrzyste_nad_Tarnowskimi_G%C3%B3rami.jpg")

        embed.description = """To polarne chmury mezosferyczne, są rzadko obserwowanymi chmurami widzianymi w półzmroku przy zmierzchu lub świcie, kiedy słońce jest 6-16 stopni poniżej horyzontu. Najczęściej obserwowane są w pasie pomiędzy 50° i 70° (północnej i południowej szerokości geograficznej). Obłoki srebrzyste są najwyższymi chmurami obserwowanymi z Ziemi, znajdują się w mezosferze około 75–85 km ponad powierzchnią."""
        embed.set_footer(text="OSWIN VHF Radar - Mesosphere")
        
        gc = await utils.gc(message.guild.id, "nlc", client)
        if gc: await gc.send(embed=embed,file= f )
        else: await message.channel.send(embed=embed,file= f)











