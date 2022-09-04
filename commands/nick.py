from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint


# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Nick(BaseCommand):

    def __init__(self):
        description = ""
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        msg = ""

        if message.author.mention == "<@188721035133059072>":
            await client.user.edit(nick="zzzzzzzz")
            print(client.user)
        #await message.channel.send(msg)
