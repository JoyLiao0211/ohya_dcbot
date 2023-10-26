import discord
# import numpy
import os
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time

"on reactions related"
"================================================================================="

async def reaction_roles_add(payload):
    if not os.path.exists(f"./bot_data/reaction_roles/{payload.message_id}.txt"):
        return
    with open(f"./bot_data/reaction_roles/{payload.message_id}.txt","r") as f:
        role_map=eval(f.read())
    if str(payload.emoji) in role_map:
        guild=client.get_guild(payload.guild_id)
        role=guild.get_role(role_map[str(payload.emoji)])
        print(payload.emoji,role.name)
        await payload.member.add_roles(role)

async def reaction_roles_remove(payload):
    if not os.path.exists(f"./bot_data/reaction_roles/{payload.message_id}.txt"):
        return
    with open(f"./bot_data/reaction_roles/{payload.message_id}.txt",'r') as f:
        role_map=eval(f.read())
    if payload.emoji in role_map:
        guild=client.get_guild(payload.guild_id)
        role=guild.get_role(role_map[str(payload.emoji)])
        await payload.member.remove_roles(role)



async def i_am_the_new_carl(payload):
    # if payload.message.channel==1155506632575418409: #拿身分組
        # await reaction_roles_add(payload)
        return
    

"on message related"
"================================================================================="

async def pick_color(message):
    if message.channel.id !=1137437517092761741 and message.channel.id!=1162707874464682115: # 拿身分組,測雞
        return
    print(message.content,"pick color")
    mes_lst=message.content.split()
    if mes_lst[0]=="許願顏色" and len(mes_lst)==2: 
        role,groles=None,{roll.name:roll for roll in message.guild.roles}
        colour=discord.Colour.from_str(message.content.split()[1])
        if message.author.name in groles:
            role=groles[message.author.name]
        else:
            role=await message.guild.create_role(name=message.author.name)
            await message.author.add_roles(role)
        print(message.author.name,role.name)
        await role.edit(colour=colour,position=44)
        await message.channel.send("給你ㄌ")
        

def format(message):
    str=(message.content).lower()
    for member in message.guild.members:
        str=str.replace(f"<@{member.id}>",f"{member.display_name}")
    for emoji in message.guild.emojis:
        str=str.replace(f"{emoji.id}","")
    return str

async def check_3_same_message(message):
    last3_mes=[mes async for mes in message.channel.history(limit=3)]
    cont_same=(len(set([mes.content for mes in last3_mes]))==1 and all([(not mes.author.bot) for mes in last3_mes]))
    auth_same=(len(set([mes.author.id for mes in last3_mes]))==1)
    if cont_same:
        print(message.content)
        await message.channel.send(f"{message.content[:min(len(message.content),200)]} (<@{message.author.id}> 自己講了三次)") if auth_same else await message.channel.send(f"{message.content[:min(len(message.content),200)]}")

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
        
distribution={}
async def pick_someone(message):
    global distribution
    with open("bot_data/distr.txt","r") as file:
        distribution=eval(file.read())
    if message.author.id not in distribution:
        distribution[message.author.id]=1
    x=distribution[message.author.id]
    distribution[message.author.id]+=(50/(x+10)/(x+2))
    distribution.update({member.id:1 for member in message.guild.members if member.id not in distribution})
    distribution={key:value for key,value in distribution.items() if key in [mem.id for mem in message.guild.members]}
    s=sum([value for key,value in distribution.items()])
    distribution={key:value*1000/s for key,value in distribution.items()}
    print(f"distribution[{message.author.name}]={distribution[message.author.id]}")
    if message.content == "抽到我的機率":
        await message.channel.send(f"抽到 {message.author.name} 的機率是 {int(distribution[message.author.id])/10} %")
    elif message.content == "我的活網程度":
        a=[[m.id,(distribution[m.id] if m.id in distribution else 0)] for m in message.guild.members]
        a.sort(key=lambda x: x[1])
        clrs=["red" if e[0] == message.author.id else "blue" for e in a] 
        plt.bar([str(len(a)-i) if a[i][0]==message.author.id else (" "*(i+1)) for i in list(range(len(a)))],[e[1]/1000 for e in a], color = clrs)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{100 * y:.0f}%'))
        file_path=f'bot_data/img_temp/{message.author.id}_bar_chart.png'
        plt.savefig(file_path, dpi=300)
        f = discord.File(file_path)
        await message.channel.send(file=f)
        plt.clf()
        if os.path.exists(file_path):
            os.remove(file_path)
    elif "抽一個人" in message.content:
        chosenid = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
        await message.channel.send(f"抽到 <@{chosenid}> 了",allowed_mentions=discord.AllowedMentions(users=False))
    with open("bot_data/distr.txt","w") as file:
        file.write(str(distribution))
    upd_members(message.guild)

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
        # if handle_map[member.id]["rating"] == rating:
        #     continue
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

last_che_message = None
async def default_react(message):
    if message.author.id==764866433120206848: # 我
        pass
    if message.author.id==844093945616269323 and random.random() < 0.5: #arctan
        await message.add_reaction("<:hao:1163133973795446935>")
    if message.author.id==531136458317365258 and "橡皮筋" in message.content: #tmp
        await message.add_reaction("🛐")
    if message.author.id==574212455786348556 and random.random() < 0.5: #ktbk
        await message.add_reaction("🧲")
    str=format(message)
    cp8w=["8w"]
    if (message.author.id==364761561866174465 and "wiwi" in str) or (message.author.id==331730758555402240 and "8e7" in str) or sum([1 if cp in str else 0 for cp in cp8w]) > 0:
        await message.add_reaction("8️⃣") and await message.add_reaction("🇼") and await message.add_reaction("🇨") and await message.add_reaction("🇵")
        return
    eights,no_eights=["8","eight","八","8️⃣","８","🎱"],["8w"]
    if sum([1 if eight in str else 0 for eight in eights]) > 0 and sum([1 if noteight in str else 0 for noteight in no_eights]) == 0:
        await message.add_reaction("8️⃣")
    if sum([1 if sad in str else 0 for sad in ["封鎖"]]) > 0:
        await message.add_reaction("😢")

async def default_reply(message):
    str=format(message)
    yege_str=list("野格炸彈我的最愛")
    if str in yege_str:
        index=yege_str.index(str)+1
        if index<len(yege_str) and "".join([mes.content async for mes in message.channel.history(limit=index)][::-1])=="".join(yege_str[:index]):
            await message.channel.send(yege_str[index])
    
    for e in [e for e in ["早安","午安","晚安"] if e in str]:
        await message.channel.send(e+("寶" if message.author.id in [764866433120206848] else ""))
    if sum([1 if a in str else 0 for a in ["真假","真的假的"] ]) > 0:
        await message.channel.send(random.choice(["當然是","怎麼可能是"])+random.choice(["真的","假的"]))
    if sum([1 if Q in str else 0 for Q in ["qq","哭哭"]])>0:
        await message.channel.send("哈哈哈")
    if sum([1 if X in str else 0 for X in ["xx","XX","插","好日子"]])>0:
        await message.channel.send("https://media.discordapp.net/attachments/1159739169996812342/1159739748148052038/ezgif-1-fa359b3a1a.gif?ex=65321ece&is=651fa9ce&hm=65ca5f62d04aa6f1807bd30c8c7f9d240856cc60b41f17a336e760b99abac83e&")
    zhong_reply_map={
        "需要解釋":"# 我需要解釋", "教授對不起":"# 教授對不起", "我不會git":"# 我不會ＧＩＴ","施廣霖":"# 施～廣～霖～"
    }
    for key in [key for key in zhong_reply_map if key in str]:
        await message.channel.send(zhong_reply_map[key])
    if sum([1 if e in str else 0 for e in ["抽到我了","抽到我ㄌ"]])>0:
        await message.channel.send(f"抽到 <@{message.author.id}> 了",allowed_mentions=discord.AllowedMentions(users=False))
    if message.author.id==527891741055909910: #cheissmart
        str="".join([format(mes) async for mes in message.channel.history(limit=2) if mes.author.id==527891741055909910])
        bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
        Pi,Chi,p7=['p','批','pea'], ['7','seven','chy','七'], ['cco','闖關',"peachy"]
        not_p7=["account"]
        for e in not_p7:
            str=str.replace(e," ")
        print("formatedstr =",str)
        if (sum([1 if e in str else 0 for e in Pi])>0 and sum([1 if e in str else 0 for e in Chi])>0) or sum([1 if all(list(str).count(c)>=e.count(c) for c in e) else 0 for e in p7])>0:
            bochi_msg=await message.channel.send(bochi_smh)
            await bochi_msg.add_reaction("🗑️")

"general stuff"
"================================================================================="

last_upd_time=None
async def check_ver(message):
    if(message.content=="check ver"):
        await message.channel.send(f"last upd: {last_upd_time}, {datetime.timedelta(seconds=int((datetime.datetime.now()-last_upd_time).total_seconds()))} ago")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    global last_upd_time
    last_upd_time=datetime.datetime.now().replace(microsecond=0)
    guilds = [guild async for guild in client.fetch_guilds(limit=1)]
    guild=guilds[0]
    roles=await guild.fetch_roles()
    print([role.position for role in roles])
    print(max([role.position for role in roles]))
    # channel = client.get_channel(1157685969135345785)
    # message = await channel.fetch_message(1166289020913987634)
    # reactions=message.reactions
    # [[print(reaction.emoji,user.name) async for user in reaction.users()] for reaction in reactions]
    print("on ready")

@client.event
async def on_message(message):
    # print(f"{message.author.display_name}, {message.author.global_name}, {message.author.name}")
        
    # bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
    # return
    if message.author==client.user or message.author.bot:
        
        return
    if message.channel.id == 1162707874464682115: #哦鴨測機
        print("測機")
        # bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
        # await message.channel.send(bochi_smh)
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
    await Baluting_board(message)
    await default_react(message)
    await default_reply(message)
    await pick_color(message)

@client.event
async def on_raw_reaction_add(payload):
    user=payload.member
    if user.bot:
        return 
    print(payload.emoji,user.name)
    bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
    if payload.emoji=="🀄":
        await payload.message.add_reaction("🀄")
    if payload.channel_id==1155506632575418409: #拿身分組
        await reaction_roles_add(payload)

    elif user.id!=527891741055909910 and payload.emoji=="🗑️" and payload.message.author==client.user and payload.message.content==bochi_smh:
        await payload.message.delete()

async def on_raw_reaction_remove(payload):
    if payload.member.bot:
        return
    if payload.channel_id==1155506632575418409: #拿身分組
        await reaction_roles_remove(payload)

if __name__ == "__main__":
    TOKEN=""
    with open("../data.txt","r") as data:
        TOKEN=eval(data.read())["TOKEN"]
    client.run(TOKEN)
    print("owo??")

