import discord
import datetime
import asyncio
from bot_data import cf
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents = intents)

"============================================================================"

async def upd_cf_roles(guild):
    with open("bot_data/handle/handle.txt","r") as f:
        handle_map=eval(f.read())
    role_ids=[1164186643129970789,1164186598338998342,1164186553606733824]
    roles=[guild.get_role(roid) for roid in role_ids]
    for member in guild.members:
        if member.id not in handle_map:
            continue
        rating=-1
        while rating < 0:
            time.sleep(2)
            rating=cf.get_rating(handle_map[member.id]["handle"])
            print(rating)
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

"============================================================================"

@client.event
async def on_ready():
    guild=client.guilds[0]
    cf_channel=await guild.fetch_channel(1162757642045903009)
    next_upd=datetime.datetime.now()
    next_upd=next_upd.replace(hour=6,minute=0,second=0,microsecond=0)
    print("owo")
    await upd_cf_roles(guild)
    print("owo2")
    await cf_channel.send("updated cf roles!")
    print("owo3")
    while True:
        time_now=datetime.datetime.now()
        sleeptime=int((next_upd-time_now).total_seconds())
        while sleeptime < 0:
            next_upd=next_upd+datetime.timedelta(days=1)
            sleeptime=int((next_upd-time_now).total_seconds())
        print(f"sleeping {sleeptime} seconds. see you next morning!")
        await asyncio.sleep(sleeptime)
        await upd_cf_roles(guild)
        await cf_channel.send("updated cf roles!")
        print("done")

if __name__ == "__main__":
    TOKEN=""
    with open("../data.txt","r") as data:
        TOKEN=eval(data.read())["TOKEN"]
    client.run(TOKEN)
