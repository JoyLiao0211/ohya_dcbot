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

async def pick_someone_old(message):
    if "抽一個人" not in message.content:
        return
    members=message.guild.members
    member_cnt=len(message.guild.members)
    i=numpy.random.randint(0,member_cnt)
    await message.channel.send(f"抽到 <@{members[i].id}> 了")

async def QQhahaha(message):
    QQ=["qq","QQ","qQ","Qq","哭哭"]
    for Q in QQ:
        if Q in message.content:
            await message.channel.send("哈哈哈")
            return

async def CFhandle(message):
    if message.channel.id!=1162757642045903009: #CF手把
        return
    message_list=message.content.split()
    if len(message_list)!=2 or message_list[0]!="!CFhandle":
        await message.channel.send("fail")
        return
    handle={}
    with open("bot_data/handle/time.txt","r") as time:
        t=int(time.read())
    with open(f"bot_data/handle/handle_{t}.txt","r") as file:
        handle=eval(file.read())
    overwrite=False
    prehandle=""
    if message.author.id in handle:
        # global overwrite,prehandle
        overwrite=True
        prehandle=handle[message.author.id]
    handle[message.author.id]=message_list[1]
    t+=1
    with open(f"bot_data/handle/handle_{t}.txt","w") as file:
        file.write(str(handle))
    with open("bot_data/handle/time.txt","w") as time:
        time.write(str(t))
    if overwrite:
        await message.channel.send(f"successfully overwrite {message.author.name} 's handle from {prehandle} to {message_list[1]}, time stamp: {t}")
    else:
        await message.channel.send(f"successfully set {message.author.name} 's handle to {message_list[1]}, time stamp: {t}")

last=0
async def Baluting_board(message):
    mes_list=message.content.split()
    if mes_list[0] != "!Baluting":
        return
    welcome="===============================\nWelcome to CSIE Baluting board!\n===============================\n"
    line="===============================\n"
    cmd="Please enter your command (post/pull/exit):"
    if len(mes_list)==1:
        await message.channel.send("```\n"+welcome+cmd+"\n```")
        return
    global last
    if mes_list[1] == "post":
        if len(mes_list) != 4:
            await message.channel.send("wrong format! correct format:\n```\n!Baluting post <from> <content>\n```")
            return
        maxl=100
        if len(mes_list[2])>maxl:
            mes_list[2]=mes_list[2][:maxl]
        if len(mes_list[3])>maxl:
            mes_list[3]=mes_list[3][:maxl]
        mes_list[2]=mes_list[2].replace("`","ˋ")
        mes_list[3]=mes_list[3].replace("`","ˋ")
        new_post=[mes_list[2],mes_list[3]]
        with open("bot_data/baluting/board.txt","r") as file:
            board=eval(file.read())
        empty=False
        for i in range(10):
            if board[(last+i)%10] == ["",""]:
                board[(last+i)%10] = new_post
                last=(last+i+1)%10
                empty=True
                break
        if not empty:
            board[last]=new_post
            last=(last+1)%10
            
        with open("bot_data/baluting/board.txt","w") as file:
            file.write(str(board))
        with open("bot_data/baluting/board_display.txt","w") as file:
            file.write("```\n")
            file.write(welcome)
            for i in range(10):
                if board[i]!=["",""]:
                    file.write("From: "+board[i][0]+"\n")
                    file.write("Content:\n"+board[i][1]+"\n")
            file.write(line)
            file.write("```\n")
        await message.channel.send("success post!")
        return
    elif mes_list[1] == "pull":
        with open("bot_data/baluting/board_display.txt","r") as file:
            board_content=file.read()
        await message.channel.send(board_content)
    elif mes_list[1] == "exit":
        exit_message=["# THERE IS NO EXIT","# JUST BALUTING"]
        await message.channel.send(exit_message[numpy.random.randint(len(exit_message))])

async def XXlee(message):
    XXlst=["xx","XX","插","好日子"]
    flg=False
    str=message.content.lower()
    for XX in XXlst:
        if XX in str:
            await message.channel.send("https://media.discordapp.net/attachments/1159739169996812342/1159739748148052038/ezgif-1-fa359b3a1a.gif?ex=65321ece&is=651fa9ce&hm=65ca5f62d04aa6f1807bd30c8c7f9d240856cc60b41f17a336e760b99abac83e&=&width=800&height=800")
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
    print(f"distribution[{message.author.name}]={distribution[message.author.id]}")
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
    if "抽到我了" not in message.content:
        return
    await message.channel.send(f"抽到 <@{message.author.id}> 了",allowed_mentions=discord.AllowedMentions(users=False))

async def zhong(message):
    zhong_reply_map={
        "需要解釋":"# 我需要解釋",
        "我不知道":"# 我不知道",
        "教授對不起":"# 教授對不起",
        "我不會git":"# 我不會ＧＩＴ"
    }
    str=message.content.lower()
    for key in zhong_reply_map.keys():
        if key in str:
            await message.channel.send(zhong_reply_map[key])
    zhong_react_list=["你要不要承認"]
    for key in zhong_react_list:
        if key in str:
            await message.add_reaction("🀄")
            break

async def default_react(message):
    # if message.channel.id==1162707874464682115: #哦鴨測機
    # if message.author.id==764866433120206848: # 我
    if message.author.id==844093945616269323: #arctan
        await message.add_reaction("<:hao:1163133973795446935>")
    without_mention=message.content.lower()
    for member in message.guild.members:
        without_mention=without_mention.replace(f"<@{member.id}>",f"{member.name}")
    # print(without_mention)
    eights=["8","eight","八","8️⃣","８","🎱"]
    for eight in eights:
        if eight in without_mention:
            await message.add_reaction("8️⃣")
            break

async def check_ver(message):
    if(message.content=="check ver"):
        await message.channel.send("last upd: 23-10-17 14:26")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents = intents)
# server = None


@client.event
async def on_ready():
    print("on ready")

@client.event
async def on_message(message):
    # if message.channel.id != 1162707874464682115: #哦鴨測機
    #     return
    # print("測機")
    if message.author==client.user:
        return
    if len(message.content)==0:
        return
    if message.channel.id==1157685969135345785: # 重要訊息
        return
    await check_3_same_message(message)
    await CFhandle(message)
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