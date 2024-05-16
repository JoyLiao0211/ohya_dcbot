import codeforces_api as cf
import numpy as np
import datetime

cp=cf.CodeforcesApi()

def handle_exist(handle:str):
    return True
    # todo

def get_rating(handle:str):
    try:
        lst=cp.user_rating(handle)
        return (lst[-1].new_rating)
    except:
        return -1

def last_submit(handle:str):
    try:
        last_sub=cp.user_status(handle,count=1)[0]
        ret={}
        ret["contest"]=last_sub.problem.contest_id
        ret["verdict"]=last_sub.verdict
        return ret
    except:
        return -1

def gen_contest_id():
    contest_list=cp.contest_list()[50:200]
    l=len(contest_list)
    while True:
        i=np.random.randint(l)
        contest=contest_list[i]
        if contest.phase=="FINISHED" and "Codeforces" in contest.name:
            return contest.id

def send_request(user_id:int,handle:str):
    if not handle_exist(handle):
        return "handle does not exist"
    request={}
    request["handle"]=handle
    request["contest"]=gen_contest_id()
    request["time"]=datetime.datetime.now()
    with open("bot_data/handle/request.txt","r") as f:
        requests=eval(f.read())
    requests[user_id]=request
    with open("bot_data/handle/request.txt","w") as f:
        f.write(str(requests))
    ret=f"Success request!\nPlease make a CE submission to any problem in contest {request['contest']} in 5 minutes.\n"
    ret+="When you are done, type in `verify` in this channel, and I'll check your last submission to verify!\n"
    return ret

def check(user_id:int):
    with open("bot_data/handle/request.txt","r") as f:
        requests=eval(f.read())
    if user_id not in requests:
        return "RE (you have no request)"
    request=requests[user_id]
    requests.pop(user_id)
    with open("bot_data/handle/request.txt","w") as f:
        f.write(str(requests))
    tnow=datetime.datetime.now()
    tstart=request["time"]
    if (tnow-tstart).total_seconds()>300:
        return "TLE (time limit: 5 minutes)"
    lastsub=last_submit(request["handle"])
    # print(lastsub)
    # print(request["contest"],'COMPILATION_ERROR')
    if lastsub["contest"]==request["contest"] and lastsub["verdict"]=='COMPILATION_ERROR':
        # store
        with open("bot_data/handle/handle.txt","r") as f:
            handle_dict=eval(f.read())
        if user_id not in handle_dict:
            handle_dict[user_id]={}
        handle_dict[user_id]["handle"]=request["handle"]
        handle_dict[user_id]["rating"]=1
        with open("bot_data/handle/handle.txt","w") as f:
            f.write(str(handle_dict))
        return f"AC (successfully set your handle to {request['handle']})"
    else:
        return "WA (fail)"
    