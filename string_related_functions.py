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

def subsequence(a:str,b:str,case_sensitive=False)->str:
    if not case_sensitive:
        a,b=a.lower(),b.lower()
    it=iter(b)
    return all(c in it for c in a)

def subsequence_list(lst:list,b:str,case_sensitive:bool=False)->bool:
    return any(subsequence(a,b,case_sensitive) for a in lst)

def subsequence_map(mp:map,b:str,case_sensitive:bool=False)->list:
    ret=[]
    for ke in mp:
        if subsequence(ke,b,case_sensitive):
            ret.append(mp[ke])
    return ret

def substring(a:str,b:str,case_sensitive:bool=False)->bool:
    if not case_sensitive:
        a,b=a.lower(),b.lower()
    return a in b

def substring_list(lst:list,b:str,case_sensitive:bool=False)->bool:
    return any(substring(a,b,case_sensitive) for a in lst)

def substring_map(mp:map,b:str,case_sensitive:bool=False)->list:
    ret=[]
    for ke in mp:
        if substring(ke,b,case_sensitive):
            ret.append(mp[ke])
    return ret

def format(message)->str:
    str=(message.content)
    for member in message.guild.members:
        str=str.replace(f"<@{member.id}>",f"{member.display_name}")
    for emoji in message.guild.emojis:
        str=str.replace(f"{emoji.id}","")
    return str