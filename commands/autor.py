from commands.base_command  import BaseCommand
import discord, utils

class Autor(BaseCommand):

    def __init__(self):
        description = "Info o autorze bocinki."
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        embed = discord.Embed(color=0x00ff00)
        embed.title = "To wszystkie dane do stalkowania mojego autora"
        embed.description = "Jeśli czegoś tu nie ma to znaczy, że nie posiada lub nie chce się nimi dzielić."
        embed.add_field(name="Youtube", value="[ONEIRO]({:s})".format("https://www.youtube.com/user/XXXRZT/videos") )
        
        embed.add_field(name="Instagram", value="[rl_oneiro]({:s})".format("https://www.instagram.com/rl_oneiro/") )
        
        embed.add_field(name="Serwer discord", value="[Śpiochy i niewyspańce]({:s})".format("https://discord.gg/tpqyYMQ") )
        
        embed.add_field(name="Discord", value="ONEIRO#9219")
        
        
        #await message.channel.send(embed=embed)
        gc = await utils.gc(message.guild.id, "autor", client)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        
        #await message.channel.send(msg)

