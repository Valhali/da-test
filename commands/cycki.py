from commands.base_command  import BaseCommand


class Cycki(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        msg = f"Yyy... znaczy... Aaaa! Lustro chcesz, " + message.author.mention + f". To mów normalnie!\nJuż przynoszę. \n\nProszku, przeglądnij się:\nhttps://tenor.com/view/grope-shake-boobs-boobs-will-ferrell-gif-17415610"

        await message.channel.send(msg)
        await message.delete()

