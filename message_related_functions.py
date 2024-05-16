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


# my stuff
from string_related_functions import *
distribution={}
name_of_id={}
default_reply_image_db=pd.DataFrame()
last_2_messages_dict={}

def mes_init():
    global name_of_id,distribution,default_reply_image_db
    with open("bot_data/user_id_to_name.txt","r") as f:
        name_of_id=eval(f.read())
    with open("bot_data/distr.txt","r") as f:
        distribution=eval(f.read())
    default_reply_image_db=pd.read_csv("~/htdocs/reply_image.csv")
    print("mes_init():\tlen(default_reply_image_db)=",len(default_reply_image_db))

def mes_exit():
    global name_of_id,distribution,default_reply_image_db
    with open("bot_data/user_id_to_name.txt","w") as f:
        f.write(str(name_of_id))
    with open("bot_data/distr.txt","w") as f:
        f.write(str(distribution))
    default_reply_image_db.to_csv("~/htdocs/reply_image.csv",index=False)
    print("mes_exit()")

async def upd_name_of_id(guild):
    global name_of_id
    name_of_id={mem.id:[mem.display_name,mem.global_name] async for mem in guild.fetch_members()}

async def upd_image_db(keyword,link):
    global default_reply_image_db
    print(len(default_reply_image_db))
    default_reply_image_db=default_reply_image_db.append({"name":keyword,"link":link},ignore_index=True)
    print(len(default_reply_image_db))

async def upd_last2_message(guild):
    global last_2_messages_dict
    channels=await guild.fetch_channels()
    for channel in channels:
        if type(channel) not in [discord.channel.CategoryChannel, discord.channel.ForumChannel]:
            last_2_messages_dict[channel.id]= [mes async for mes in channel.history(limit=2)]

"on message related"
"================================================================================="

async def pick_color(message):
    if message.channel.id !=1137437517092761741 and message.channel.id!=1162707874464682115: # 拿身分組,測雞
        return
    # print(message.content,"pick color")
    mes_lst=message.content.split()
    if mes_lst[0]=="許願顏色" and len(mes_lst)==2: 
        role,groles=None,{roll.name:roll for roll in message.guild.roles}
        colour=discord.Colour.from_str(message.content.split()[1])
        if message.author.name in groles:
            role=groles[message.author.name]
        else:
            role=await message.guild.create_role(name=message.author.name)
            await message.author.add_roles(role)
        # print(message.author.name,role.name)
        await role.edit(colour=colour,position=44)
        await message.channel.send("給你ㄌ")

async def check_3_same_message(message):
    if message.channel.id not in last_2_messages_dict:
        last_2_messages_dict[message.channel.id]= [mes async for mes in message.channel.history(limit=3)][1:]
    last3_mes=[message]+last_2_messages_dict[message.channel.id]
    print([mes.content for mes in last3_mes])
    if len(set([mes.content for mes in last3_mes]))==1:
        last3_mes=[mes async for mes in message.channel.history(limit=3)]
    cont_same=(len(set([mes.content for mes in last3_mes]))==1 and all([(not mes.author.bot) for mes in last3_mes]))
    auth_same=(len(set([mes.author.id for mes in last3_mes]))==1)
    if len(last3_mes)==3 and cont_same:
        # print(message.content)
        await message.channel.send(f"{message.content[:min(len(message.content),200)]} (<@{message.author.id}> 自己講了三次)") if auth_same else await message.channel.send(f"{message.content[:min(len(message.content),200)]}")
    last_2_messages_dict[message.channel.id]=last3_mes[:2]
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

async def pick_someone(message):
    global distribution,name_of_id
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
    elif message.content == "活網排行榜":
        top_ten=[name_of_id[uid] for (uid,score) in (sorted(distribution.items(), key=lambda x: x[1], reverse=True)[:10])]
        output="<<活網排行榜>>\n"
        for i in range(10):
            if top_ten[i][1]==None or top_ten[i][1]==top_ten[i][0]:
                output+=f"{i+1}. {top_ten[i][0]}\n"
            else:
                output+=f"{i+1}. {top_ten[i][0]} / {top_ten[i][1]}\n"
        await message.channel.send(output)
    elif message.content == "活網排行榜 all":
        full_list=[name_of_id[uid] for (uid,score) in (sorted(distribution.items(), key=lambda x: x[1], reverse=True))]
        output="<<活網排行榜>>\n"
        for i in range(len(full_list)):
            if full_list[i][1]==None or full_list[i][1]==full_list[i][0]:
                output+=f"{i+1}. {full_list[i][0]}\n"
            else:
                output+=f"{i+1}. {full_list[i][0]} / {full_list[i][1]}\n"
        await message.channel.send(output)
    elif "抽一個人" in message.content:
        chosenid = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
        if ("mention" in message.content):
            await message.channel.send(f"抽到 <@{chosenid}> 了 (mention)")
        else:
            await message.channel.send(f"抽到 <@{chosenid}> 了",allowed_mentions=discord.AllowedMentions(users=("mention" in message.content)))


async def upd_cf_roles(guild): # 沒在維護
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
        # print(member.name,lst,rating)
    with open("bot_data/handle/handle.txt","w") as f:
        f.write(str(handle_map))


async def default_react(message):
    if message.channel.id==1168203729267326986: #支語database
        await message.add_reaction("🇨🇳")
    if message.channel.id in [1217743906582827049,1162707874464682115]: # 投稿圖片, 測機
        if message.content!="" and len(message.attachments)==1:
            await message.add_reaction("✅")
    if message.channel.id == 1229722177146982400: #語錄評比
        print("語錄評比")
        await message.add_reaction("❤️")
        await message.add_reaction("⛽")
        await message.add_reaction("😮")
        await message.add_reaction("😭")
        await message.add_reaction("😆")
    if message.author.id==764866433120206848: # 我
        pass
    if message.author.id==844093945616269323 and random.random() < 0.5: #arctan
        await message.add_reaction("<:hao:1163133973795446935>")
    if message.author.id==531136458317365258 and substring("橡皮筋", message.content): #tmp
        await message.add_reaction("🛐")
    if message.author.id==574212455786348556 and random.random() < 0.5: #ktbk
        await message.add_reaction("🧲")
    str=format(message)
    eights=["**8**","8️⃣"]
    if sum([1 if eight in str else 0 for eight in eights]) > 0:
        await message.add_reaction("8️⃣")
    if sum([1 if substring(sad,str) else 0 for sad in ["封鎖"]]) > 0:
        await message.add_reaction("😢")

async def default_reply(message):
    str=format(message)
    if substring("吃什麼",str):
        place_map={
            "118":["小圓村","老哥","新丼","旭倉咖哩","唯雞館","樂和","笑嘻嘻","五九","二八","阿孟","方最","Im Pasta","Barkers","呈信鵝肉飯","Poke","叮叮","韓喜堂","大李水餃","烤肉飯"],
            "公館":["12迷你","夜市","順園","水源二樓","半則製麵","赤神","隱家","山嵐","新天地","雪腐","鍋in","subway","吉天元","肯德基","捲餅","吉野家","Sukiya","漢堡王","新馬辣","小飯館","麥子磨麵","老先覺"],
            "活大":["麥當勞","四海遊龍","素食","OK mart","邱食堂","自助餐"],
            "女九":["水餃","滷味","自助餐","果汁"]
        }
        food_lst=sum((substring_map(place_map,str)),[])
        if len(food_lst)==0:
            food_lst=sum((place_map[key] for key in place_map),[])
        await message.channel.send(f"吃 {random.choice(food_lst)}")
    yege_str=list("野格炸彈我的最愛")
    if str in yege_str:
        index=yege_str.index(str)+1
        if index<len(yege_str) and "".join([mes.content async for mes in message.channel.history(limit=index)][::-1])=="".join(yege_str[:index]):
            await message.channel.send(yege_str[index])
    bao=[764866433120206848]
    if str=='寶' and message.author.id not in bao:
        await message.channel.send("誰你寶")
    for e in [e for e in ["早安","午安","晚安"] if e in str]:
        await message.channel.send(e+("寶" if message.author.id in bao else ""))
    # if sum([1 if substring(a,str) else 0 for a in ["真假","真的假的"] ]) > 0:
    if substring_list(["真假","真的假的"],str):
        await message.channel.send(random.choice(["當然是","怎麼可能是"])+random.choice(["真的","假的"]))
    # if sum([1 if substring(Q,str) else 0 for Q in ["qq","哭哭"]])>0:
    if substring_list(["qq","哭哭"],str):
        await message.channel.send("哈哈哈")
    # if sum([1 if substring(X,str) else 0 for X in ["xx","XX","插","好日子"]])>0:
    if substring_list(["xx","XX","插","好日子"],str,True):
        xxlee=await message.guild.fetch_sticker(1154854490084753550)
        await message.channel.send(stickers=[xxlee])
        # await message.channel.send("https://media.discordapp.net/attachments/1159739169996812342/1159739748148052038/ezgif-1-fa359b3a1a.gif?ex=65321ece&is=651fa9ce&hm=65ca5f62d04aa6f1807bd30c8c7f9d240856cc60b41f17a336e760b99abac83e&")
    zhong_reply_map={
        "我需要解釋":"# 我需要解釋", "教授對不起":"# 教授對不起", "我不會git":"# 我不會ＧＩＴ", "施廣霖":"# 施～廣～霖～"
    }
    for a in subsequence_map(zhong_reply_map,str):
        await message.channel.send(a)
    # if sum([1 if substring(e,str) else 0 for e in ["抽到我了","抽到我ㄌ"]])>0:
    if substring_list(["抽到我了","抽到我ㄌ"],str):
        await message.channel.send(f"抽到 <@{message.author.id}> 了",allowed_mentions=discord.AllowedMentions(users=False))
    if message.author.id==527891741055909910: #cheissmart
        messages=[mes async for mes in message.channel.history(limit=10)]
        messages=[list(group) for key, group in groupby(messages, lambda x: x.author.id==message.author.id) if key][0][::-1]
        str=" ".join([format(mes) for mes in messages])
        bochi_muli=await message.guild.fetch_sticker(1150667766827851846)
        # bochi_smh="https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768"
        Pi,Chi,p7=['p','批','pea'], ['7','seven','chy','七'], ['cco','闖關',"peachy"]
        not_p7=["account"]
        for e in not_p7:
            str=str.replace(e," ")
        # print("formatedstr =",str)
        # if (sum([1 if e in str else 0 for e in Pi])>0 and sum([1 if e in str else 0 for e in Chi])>0) or sum([1 if all(list(str).count(c)>=e.count(c) for c in e) else 0 for e in p7])>0:
        if (substring_list(Pi,str) and substring_list(Chi,str)) or (subsequence_list(p7,str)):
            bochi_msg=await message.channel.send(stickers=[bochi_muli])
            await bochi_msg.add_reaction("🗑️")

def lcs_sequence_length(keyword, message_content):
    # Get the length of both strings
    len_keyword = len(keyword)
    len_message = len(message_content)
    
    # Create a 2D list to store lengths of longest common subsequence.
    lcs_table = [[0] * (len_message + 1) for _ in range(len_keyword + 1)]
    
    # Build the lcs_table from the bottom up
    for i in range(1, len_keyword + 1):
        for j in range(1, len_message + 1):
            if keyword[i - 1] == message_content[j - 1]:
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
            else:
                lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])
    
    # lcs_table[len_keyword][len_message] contains the length of LCS for keyword and message_content
    return lcs_table[len_keyword][len_message]


async def default_reply_w_image(message):
    global default_reply_image_db
    print("defa..():\tlen(default_reply_image_db)=",len(default_reply_image_db))
    max_length,matching_link = 0,None
    for keyword, link in zip(default_reply_image_db['name'],default_reply_image_db['link']):
        meslen,keylen=len(message.content),len(keyword)
        lcslen = lcs_sequence_length(keyword,message.content)
        if (lcslen > meslen*0.7) and (lcslen > keylen*0.7) and (lcslen >= min(5,keylen)):
            if lcslen > max_length:
                max_length = lcslen
                matching_link = link
    if matching_link!=None:
        await message.channel.send(matching_link)
