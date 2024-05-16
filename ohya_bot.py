# library stuff
import sys
sys.path.append("../discord_py/")
import discord
import os
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time
from itertools import groupby
import pandas as pd
import atexit

# my stuff
from string_related_functions import *
from reaction_related_functions import *
from message_related_functions import *
TOKEN=""
guild=None
testing_channel=None
edited_channel=None
delete_channel=None

debug=False
if(len(sys.argv)>1 and sys.argv[1]=="debug"):
    debug=True
    print("debug run")

last_upd_time=None
async def check_ver(message):
    if(message.content=="check ver"):
        await message.channel.send(f"last upd: {last_upd_time}, {datetime.timedelta(seconds=int((datetime.datetime.now()-last_upd_time).total_seconds()))} ago")
        # await message.channel.send("修理中可能會常常下線QQ")

intents = discord.Intents.all()
client = discord.Client(intents = intents)

def init():
    global last_upd_time,name_of_id,TOKEN
    last_upd_time=datetime.datetime.now().replace(microsecond=0)
    with open("../data.txt","r") as f:
        TOKEN=eval(f.read())["TOKEN"]
    mes_init()
    if not debug:
        with open("logfile","a") as f:
            f.write(f"[{datetime.datetime.now().replace(microsecond=0)}]  starting dcbot\n")
        atexit.register(on_exit)


def on_exit():
    mes_exit()
    with open("logfile","a") as f:
            f.write(f"[{datetime.datetime.now().replace(microsecond=0)}]  terminating dcbot\n")
    print("on_exit()")

@client.event
async def on_ready():
    global guild, testing_channel, edited_channel, delete_channel
    guild = [guild async for guild in client.fetch_guilds(limit=1)][0]
    testing_channel = await guild.fetch_channel(1162707874464682115)
    edited_channel  = await guild.fetch_channel(1231222683279036536)
    delete_channel  = await guild.fetch_channel(1231222802477219910)
    await upd_name_of_id(guild)
    await upd_last2_message(guild)
    print("on ready")

@client.event
async def on_message(message):
    if message.author==client.user or message.author.bot:
        return
    global debug
    if message.channel.id == 1162707874464682115: #哦鴨測機
        print("測機")
    elif debug:
        return
    if message.channel.id==1162757642045903009: # CF手把
        await CFhandle(message)
        return
    if len(message.content)==0:
        return
    if message.channel.id==1157685969135345785: # 重要訊息
        return
    await check_3_same_message(message)
    await check_ver(message)
    if message.channel.id==1141778910955180032: # 真的依某
        return
    await pick_someone(message)
    await default_react(message)
    await default_reply(message)
    await default_reply_w_image(message)
    await pick_color(message)

@client.event
async def on_message_edit(before, after):
    if before.author==client.user or before.author.bot:
        return
    if before.content==after.content:
        return
    output=""
    output=f"**{before.author.name} edited a message!**\n"
    output+=f"**channel:<#{before.channel.id}>**\n"
    output+=f"**message:**{before.jump_url}\n"
    output+="**before:**\n"
    output+=before.content
    output+="\n**after:**\n"
    output+=after.content
    await edited_channel.send(output)

@client.event
async def on_message_delete(message):
    if message.author==client.user or message.author.bot:
        return
    output=f"**{message.author.name} deleted a message!**\n"
    output+=f"**channel:<#{message.channel.id}>**\n"
    output+="**message.content:**\n"
    output+=message.content
    await delete_channel.send(output)


async def get_message_from_payload(payload):
    guild=client.get_guild(payload.guild_id)
    channel=await guild.fetch_channel(payload.channel_id)
    message=await channel.fetch_message(payload.message_id)
    return message

@client.event
async def on_raw_reaction_add(payload):
    user=payload.member
    message=await get_message_from_payload(payload)
    if user.bot:
        return 
    print(payload.emoji,user.name)
    await submit_image(payload,message)
    bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
    if payload.emoji=="🀄":
        await message.add_reaction("🀄")
    if payload.channel_id==1155506632575418409: #拿身分組
        await reaction_roles_add(payload)
    if str(payload.emoji)=="🗑️" and message.author.id==client.user.id:
        await message.delete()


async def on_raw_reaction_remove(payload):
    message=await get_message_from_payload(payload)
    if payload.member.bot:
        return
    if payload.channel_id==1155506632575418409: #拿身分組
        await reaction_roles_remove(payload,message)
    # if payload.channel_id!=1168203729267326986: #database
    #     await china_react_rmv(payload)

async def on_raw_member_remove(payload):
    channelid=1155507142321778768 # modlog
    channel=await guild.fetch_channel(channel_id=channelid)
    await channel.send(f"{payload.user.name} 剛剛離開了")

async def on_raw_member_remove(payload):
    channelid=1155507142321778768 # modlog
    channel=await guild.fetch_channel(channel_id=channelid)
    await channel.send(f"{payload.user.name} 剛剛離開了")

async def on_member_join(member):
    channelid=1155507142321778768 # modlog
    guild=member.guild
    channel=await guild.fetch_channel(channel_id=channelid)
    await channel.send(f"{member.name} 剛剛進來了")

if __name__ == "__main__":
    init()
    client.run(TOKEN)
