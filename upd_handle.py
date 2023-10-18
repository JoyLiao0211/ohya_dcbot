import discord
import time


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents = intents)

# ============================================================================ #

async def upd_cf_roles(guild):
    from bot_data import cf
    import time
    with open("bot_data/handle/handle.txt","r") as f:
        handle_map=eval(f.read())
    role_ids=[1164186643129970789,1164186598338998342,1164186553606733824]
    roles=[guild.get_role(roid) for roid in role_ids]
    for member in guild.members:
        if member.id not in handle_map:
            continue
        rating=-1
        while rating<0:
            time.sleep(0.3)
            rating=cf.get_rating(handle_map[member.id]["handle"])
        if handle_map[member.id]["rating"] == rating:
            continue
        handle_map[member.id]["rating"]=rating
        lst=[False,False,False]
        if rating >= 2100:
            lst[2]=True
        elif rating >= 1900:
            lst[1]=True
        elif rating >= 1600:
            lst[0]=True
        for i in range(3):
            if lst[i]:
                await member.add_roles(roles[i])
            elif not lst[i]:
                await member.remove_roles(roles[i])
        print(member.name,lst,rating)
    with open("bot_data/handle/handle.txt","w") as f:
        f.write(str(handle_map))

# ============================================================================ #

@client.event
async def on_ready():
    time.sleep(86400)
    await upd_cf_roles(client.guilds[0])
    print("done")

if __name__ == "__main__":
    TOKEN=""
    with open("../data.txt","r") as data:
        TOKEN=eval(data.read())["TOKEN"]
    client.run(TOKEN)