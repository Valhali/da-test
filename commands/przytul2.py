from commands.base_command  import BaseCommand
import discord, utils

class Przytul2(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        embed = discord.Embed(color=0x00ff00)
        embed.description = f"No już, już... Chodź się przytulić. :hugging: "
        embed.set_image(url="https://media1.tenor.com/images/68f16d787c2dfbf23a4783d4d048c78f/tenor.gif")
        await utils.send(client= client, message=message, cmd="przytul2",embed=embed)
