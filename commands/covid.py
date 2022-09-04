from commands.base_command  import BaseCommand
import urllib.request, json
from datetime import datetime

class Covid(BaseCommand):

    def __init__(self):
        description = "Info o zarazie. Możliwe opóźnienie z najnowszymi danymi."
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass

        with urllib.request.urlopen("https://api.covid19api.com/summary") as url:
            data = json.loads(url.read().decode())
        with urllib.request.urlopen("https://api.covid19api.com/dayone/country/poland") as url:
            data2 = json.loads(url.read().decode())[-1]
            t = datetime.strptime(data2["Date"], '%Y-%m-%dT%H:%M:%SZ') #2020-11-23T00:00:00Z"

        str1 = "**Dane globalne**: \n  Potwierdzone przypadki: **{:,}**".format(data["Global"]["TotalConfirmed"])
        str1 += " Przybyło: **{:,}**".format(data["Global"]["NewConfirmed"])
        str1 += "\n  Zmarło: **{:,}**".format(data["Global"]["TotalDeaths"])
        str1 += " Przybyło: **{:,}**".format(data["Global"]["NewDeaths"])
        str1 += "\n  Wyzdrowiało: **{:,}**".format(data["Global"]["TotalRecovered"])
        str1 += " Przybyło: **{:,}**".format(data["Global"]["NewRecovered"])


        for e in data["Countries"]:
            if e["Country"]=="Poland":
                pl = e
#=============================================================
        str1 += "\n\n**Polska** ("+t.strftime("%d-%m-%Y")+"): \n  Potwierdzone przypadki: **{:,}**".format(pl["TotalConfirmed"])
        str1 += " Przybyło: **{:,}**".format(pl["NewConfirmed"])
        str1 += "\n  Zmarło: **{:,}**".format(pl["TotalDeaths"])
        str1 += " Przybyło: **{:,}**".format(pl["NewDeaths"])
        str1 += "\n  Wyzdrowiało: **{:,}**".format(pl["TotalRecovered"])
        str1 += " Przybyło: **{:,}**".format(pl["NewRecovered"])

        msg = str1

        await message.channel.send(msg)

#  https://api.covid19api.com/dayone/country/poland