welcome="===============================\nWelcome to CSIE Baluting board!\n===============================\n"
line="===============================\n"
cmd="Please enter your command (post/pull/exit):"

def pull():
    ret=""
    with open("bot_data/baluting/board_display.txt","r") as f:
        ret=f.read()
    return ret

def post(From:str,Content:str):
    maxfrom,maxcontent=30,150
    if len(From) > maxfrom:
        From=From[:maxfrom]
    if len(Content) > maxcontent:
        Content=Content[:maxcontent]
    From = From.replace("`","ˋ")
    Content = Content.replace("`","ˋ")
    with open("bot_data/baluting/last.txt","r") as f:
        last=int(f.read())
    with open("bot_data/baluting/board.txt","r") as f:
        board=eval(f.read())
    mt=False
    for i in range(10):
        if board[(last+i)%10]==["",""]:
            board[(last+i)%10]=[From,Content]
            last=(last+i+1)%10
            mt=True
            break
    if not mt:
        board[last]=[From,Content]
        last=(last+1)%10
    with open("bot_data/baluting/last.txt","w") as f:
        f.write(str(last))
    with open("bot_data/baluting/board.txt","w") as f:
        f.write(str(board))
    with open("bot_data/baluting/board_display.txt","w") as f:
        f.write("```\n")
        f.write(welcome)
        for i in range(10):
            if board[i]!=["",""]:
                f.write("From: "+board[i][0]+"\n")
                f.write("Content:\n"+board[i][1]+"\n")
        f.write(line)
        f.write("```\n")
    return "success post!"           

def enter():
    return "```\n"+welcome+cmd+"\n```"

def exit():
    import numpy as np
    message=["# THERE IS NO EXIT","# JUST BALUTING"]
    return message[np.random.randint(len(message))]