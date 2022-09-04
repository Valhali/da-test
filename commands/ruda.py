from commands.base_command import BaseCommand
import settings, discord, json, utils

# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Ruda(BaseCommand):

    def __init__(self):
        description = "Lista komend (to co właśnie czytasz)"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        try:
            await message.delete()
        except :
            pass
        from message_handler import COMMAND_HANDLERS
        #msg = message.author.mention + "\n"
        msg=""
        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            if len(cmd[1].description)>5:
                msg += "\n" + cmd[1].description

        conn = settings.conn
        c = settings.c
        id = str(message.guild.id)
        i=[]
        odp=[]
        for i in c.execute("SELECT cmd FROM command WHERE srv=?;", (id,) ):
            if i: 
                if not i[0] in odp: odp.append(i[0])
                
        for j in c.execute("SELECT conf FROM config WHERE serwer=? and id LIKE ?;", (id,"cmd_%") ):
            if j: 
                j = json.loads(j[0])   
                cmd = j["cnfid"].replace("cmd_","")
                if not cmd in odp: odp.append(cmd)
                
                ############################
        for j in c.execute("SELECT conf FROM config WHERE serwer=? and id LIKE ?;", (id,"scmd_%") ):
            if j: 
                j = json.loads(j[0])   
                cmd = j["cnfid"].replace("scmd_","")                
                if not cmd in odp: odp.append(cmd)
                ############################
                
   
        gc = await utils.gc(message.guild.id, "ruda", client)
        embed = discord.Embed(color=0x00ff00)
        embed.title = "Lista komend" 
        embed.description = msg +"\n\nJeżeli jesteś władzą na serwerze to sprawdź [komendy dodatkowe](https://docs.google.com/document/d/1vSP5HDveWReESTi-KZ74dJW5Ab9CaIRljp1kwir0w2c/edit 'Komendy tylko dla władz serwera')."
        #await message.channel.send(embed=embed)
        if gc: await gc.send(embed=embed)
        else: await message.channel.send(embed=embed)
        if odp:
            embed=None
            embed = discord.Embed(color=0x00ff00)
            embed.title = "Lista komend własnych - tylko na ten serwer" 
            embed.description = ", ".join(odp)
            #await message.channel.send(embed=embed)
            if gc: await gc.send(embed=embed)
            else: await message.channel.send(embed=embed)