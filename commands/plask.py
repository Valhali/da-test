from commands.base_command  import BaseCommand
import discord, utils

class Plask(BaseCommand):

    def __init__(self):
        description = "Uderz!"
        params = ["@wzmianka"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        if not params[0]:
            params.append(" ")
            msg = f"Aby to zadziałało musisz użyć @wzmianki"
            #await message.channel.send(msg)
            
            await utils.send(client= client, message=message, cmd="plask",msg =msg)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.description = f"Ludek " +message.author.mention + f" przywalił "+ params[0] +f" w ryjek aż zęby chrupnęły! :open_mouth:"
            embed.set_image(url="https://media1.tenor.com/images/1ec6e9f65193cad4717ea0d31185bb75/tenor.gif")
            #await message.channel.send(embed=embed)
            await utils.send(client= client, message=message, cmd="plask",embed=embed)

