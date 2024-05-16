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
import re

# my stuff
from string_related_functions import *
from message_related_functions import upd_image_db

"on reactions related"
"================================================================================="


async def reaction_roles_add(payload,message):
    if not os.path.exists(f"./bot_data/reaction_roles/{payload.message_id}.txt"):
        return
    with open(f"./bot_data/reaction_roles/{payload.message_id}.txt","r") as f:
        role_map=eval(f.read())
    if str(payload.emoji) in role_map:
        guild=client.get_guild(payload.guild_id)
        role=guild.get_role(role_map[str(payload.emoji)])
        print(payload.emoji,role.name)
        await payload.member.add_roles(role)

async def reaction_roles_remove(payload,message):
    if not os.path.exists(f"./bot_data/reaction_roles/{payload.message_id}.txt"):
        return
    with open(f"./bot_data/reaction_roles/{payload.message_id}.txt",'r') as f:
        role_map=eval(f.read())
    if payload.emoji in role_map:
        guild=client.get_guild(payload.guild_id)
        role=guild.get_role(role_map[str(payload.emoji)])
        await payload.member.remove_roles(role)

async def submit_image(payload,message):
    print(message.content)
    if payload.channel_id in [1217743906582827049] and payload.user_id==764866433120206848: # ,1162707874464682115: 測機
        keyword=message.content
        print("keyword =",keyword)
        attachments=message.attachments
        print("len attch =", len(attachments))
        for attch in attachments:
            await upd_image_db(keyword,attch.url)
            await message.channel.send(f"new image added\nkeyword:\n{keyword}\nurl:\n{attch.url}")

async def pin_message(payload, message):
    pass