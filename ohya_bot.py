import discord
import numpy
import os
import random

last_message={}
async def check_3_same_message(message):
    global last_message
    if message.channel not in last_message:
        last_message[message.channel]=[message.content,1]
    elif message.content==last_message[message.channel][0]:
        last_message[message.channel][1]+=1
    else:
        last_message[message.channel]=[message.content,1]
    if last_message[message.channel][1]==3:
        await message.channel.send(message.content)
        last_message[message.channel][1]=0

yege={}
async def check_yegebomb(message):
    yege_str=list("野格炸彈我的最愛")
    global yege
    if message.channel not in yege:
        yege[message.channel]=0
    if message.content != yege_str[yege[message.channel]]:
        yege[message.channel]=0
    if message.content == yege_str[yege[message.channel]]:
        yege[message.channel]+=1
        if yege[message.channel] < len(yege_str):
            await message.channel.send(yege_str[yege[message.channel]])
        yege[message.channel]+=1
    if yege[message.channel] >= len(yege_str):
        yege[message.channel] = 0

async def QQhahaha(message):
    QQ=["qq","QQ","qQ","Qq","哭哭"]
    for Q in QQ:
        if Q in message.content:
            await message.channel.send("哈哈哈")
            return

async def CFhandle(message):
    from bot_data import cf
    message_list=message.content.split()
    if message_list[0]=="set":
        if len(message_list)<2:
            await message.channel.send("wrong format! correct format:```set <handle>```")
            return
        await message.channel.send(cf.send_request(message.author.id,message_list[1]))
    elif message_list[0]=="verify":
        await message.channel.send(cf.check(message.author.id))
    else:
        await message.channel.send("wrong format! correct format:```set <handle>```or```verify```")

async def Baluting_board(message):
    mes_list=message.content.split()
    if mes_list[0] != "!Baluting":
        return
    from bot_data import baluting as bl
    if len(mes_list)==1:
        await message.channel.send(bl.enter())
        return
    if mes_list[1] == "post":
        if len(mes_list) != 4:
            await message.channel.send("wrong format! correct format:\n```\n!Baluting post <from> <content>\n```")
            return
        await message.channel.send(bl.post(mes_list[2],mes_list[3]))
    elif mes_list[1] == "pull":
        await message.channel.send(bl.pull())
    elif mes_list[1] == "exit":
        await message.channel.send(bl.exit())

async def XXlee(message):
    XXlst=["xx","XX","插","好日子"]
    flg=False
    str=message.content.lower()
    for XX in XXlst:
        if XX in str:
            await message.channel.send("https://media.discordapp.net/attachments/1159739169996812342/1159739748148052038/ezgif-1-fa359b3a1a.gif?ex=65321ece&is=651fa9ce&hm=65ca5f62d04aa6f1807bd30c8c7f9d240856cc60b41f17a336e760b99abac83e&")
            return

distribution={}
async def pick_someone(message):
    global distribution
    if len(distribution)==0:
        with open("bot_data/distr.txt","r") as file:
            distribution=eval(file.read())
    if message.author.id not in distribution:
        distribution[message.author.id]=10
    distribution[message.author.id]+=0.3
    # print(f"distribution[{message.author.name}]={distribution[message.author.id]}")
    if message.content == "抽到我的機率":
        await message.channel.send(f"抽到 {message.author.name} 的機率是 {int(distribution[message.author.id])/10} %")
    elif "抽一個人" in message.content:
        s=0.0
        members=message.guild.members
        for member in members:
            if member.id not in distribution:
                distribution[member.id]=10
            s+=distribution[member.id]
        print(s)
        for key in distribution:
            distribution[key]*=1000/s
        chosenid = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
        await message.channel.send(f"抽到 <@{chosenid}> 了",allowed_mentions=discord.AllowedMentions(users=False))
    with open("bot_data/distr.txt","w") as file:
        file.write(str(distribution))

async def pick_me(message):
    message_content=message.content.replace("ㄌ","了")
    if "抽到我了" not in message.content:
        return
    await message.channel.send(f"抽到 <@{message.author.id}> 了",allowed_mentions=discord.AllowedMentions(users=False))

async def zhong(message):
    zhong_reply_map={
        "需要解釋":"# 我需要解釋",
        "我不知道":"# 我不知道",
        "教授對不起":"# 教授對不起",
        "我不會git":"# 我不會ＧＩＴ",
        "施廣霖":"# 施～廣～霖～",
        "施~廣~霖~":"# 施～廣～霖～",
        "施～廣～霖":"# 施～廣～霖～"
    }
    str=message.content.lower()
    for key in zhong_reply_map.keys():
        if key in str:
            await message.channel.send(zhong_reply_map[key])
    zhong_react_list=["你要不要承認","表揚"]
    for key in zhong_react_list:
        if key in str:
            await message.add_reaction("🀄")
            break

async def default_react(message):
    # if message.channel.id==1162707874464682115: #哦鴨測機
    #     await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
    # if message.author.id==764866433120206848: # 我
    if message.author.id==844093945616269323: #arctan
        await message.add_reaction("<:hao:1163133973795446935>")
    str=(message.content).lower()
    for member in message.guild.members:
        str=str.replace(f"<@{member.id}>",f"{member.display_name}")
    for emoji in message.guild.emojis:
        str=str.replace(f"{emoji.id}","")
    # print(str)
    if message.author.id==527891741055909910: #cheissmart ,"妻","漆","欺","棲","戚","淒"
        P7=["7","７","七","seven","柒","闖關","⑦"]
        for p7 in P7:
            if p7 in str:
                await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
                break
    eights=["8","eight","八","8️⃣","８","🎱"]
    for eight in eights:
        if eight in str:
            await message.add_reaction("8️⃣")
            break
    sadge=["封鎖"]
    for sad in sadge:
        if sad in str:
            await message.add_reaction("😢")

async def check_ver(message):
    if(message.content=="check ver"):
        await message.channel.send("last upd: 23-10-18 14:27")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("on ready")

@client.event
async def on_message(message):
    
    # print(f"{message.author.display_name}, {message.author.global_name}, {message.author.name}")
    # if message.channel.id != 1162707874464682115: #哦鴨測機
    #     return
    # print("測機")
    if message.author==client.user:
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
    await QQhahaha(message)
    await check_yegebomb(message)
    await pick_someone(message)
    await pick_me(message)
    await Baluting_board(message)
    await XXlee(message)
    await zhong(message)
    await default_react(message)
    

TOKEN=""
with open("../data.txt","r") as data:
    TOKEN=eval(data.read())["TOKEN"]
client.run(TOKEN)