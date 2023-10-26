import discord
import time


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents = intents)

# ============================================================================ #

def upd_members(guild):
    with open("bot_data/distr.txt","r") as f:
        distr=eval(f.read())
    with open("bot_data/user_id_to_name.txt","r") as f:
        name=eval(f.read())
    memid=[member.id for member in guild.members]
    pop=[]
    for key in name:
        if key not in memid:
            pop.append(key)
    for key in pop:
        name.pop(key)
    pop=[]
    for key in distr:
        if key not in memid:
            pop.append(key)
    for key in pop:
        distr.pop(key)
    with open("bot_data/distr.txt","w") as f:
        f.write(str(distr))
    with open("bot_data/user_id_to_name.txt","w") as f:
        f.write(str(name))
        

# ============================================================================ #

@client.event
async def on_ready():
    for guild in client.guilds:
        upd_members(guild)
    print("done")

if __name__ == "__main__":
    TOKEN=""
    with open("../data.txt","r") as data:
        TOKEN=eval(data.read())["TOKEN"]
    client.run(TOKEN)