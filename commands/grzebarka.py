from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint


# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Grzebarka(BaseCommand):

    def __init__(self):
        description = "Link do grzebarki"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        msg = message.author.mention +" Proszku, to link do grzebarki: http://orbit.5v.pl/tm/#panel-538950"

        await message.channel.send(msg)
        await message.delete()
