from commands.base_command  import BaseCommand
import discord, utils

class Przytul(BaseCommand):

    def __init__(self):
        description = "Przytulas wybranej osoby"
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
            await utils.send(client= client, message=message, cmd="przytul",msg=msg)
        else:
            embed = discord.Embed(color=0x00ff00)
            embed.description = message.author.mention + f" czule obejmuje "+ params[0] +f" w ramiona. :hugging: "
            embed.set_image(url="https://media1.tenor.com/images/fd47e55dfb49ae1d39675d6eff34a729/tenor.gif")
            #await message.channel.send(embed=embed)
            await utils.send(client= client, message=message, cmd="przytul",embed=embed)

