def warning(msg: str):
    print("[\033[33mWARN\033[m]\t" + msg)

def info(msg: str):
    print("[\033[36mINFO\033[m]\t" + msg)

def err(msg: str):
    print("[\033[31mERROR\033[m]\t" + msg)
    #exit(1)