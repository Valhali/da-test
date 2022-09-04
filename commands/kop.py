from commands.base_command  import BaseCommand
import discord, utils

class Kop(BaseCommand):

    def __init__(self):
        description = "Kopnij..."
        params = ["@wzmianka"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        await message.delete()
        
        if not params[0]:
            params.append(" ")
            msg = f"Aby to zadziałało musisz użyć @wzmianki"
            await message.channel.send(msg)
            await utils.send(client= client, message=message, cmd="kop",msg=msg)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.description = params[0] + f" zostaje stąd wykopany przez "+ message.author.mention
            embed.set_image(url="https://media1.tenor.com/images/dc269398c26d9d35dc016d935269008d/tenor.gif")
            #await message.channel.send(embed=embed)
            await utils.send(client= client, message=message, cmd="kop",embed=embed)