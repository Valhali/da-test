from commands.base_command  import BaseCommand
import discord, utils

class Klaps(BaseCommand):

    def __init__(self):
        description = "Daj klapsa"
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
            await utils.send(client= client, message=message, cmd="klaps",msg=msg)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.description = message.author.mention + f" klepie "+ params[0] +f" w zacny tyłeczek! :blush:"
            embed.set_image(url="https://media1.tenor.com/images/cf6a309d7b66d432ee75ee8ac7dad3c9/tenor.gif")
            #await message.channel.send(embed=embed)
            await utils.send(client= client, message=message, cmd="klaps",embed=embed)
