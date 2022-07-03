import datetime
import random

import colorama; colorama.init()


def log(info, level="info"):
    color = None
    prefix = None

    if level == "info":
        color = colorama.Fore.WHITE
        prefix = "[INFO]"
    elif level == "request":
        color = colorama.Fore.WHITE
        prefix = "[REQUEST]"
    elif level == "warning":
        color = colorama.Fore.YELLOW
        prefix = "[WARNING]"
    elif level == "critical":
        color = colorama.Fore.RED
        prefix = "[CRITICAL]"

    stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"{stamp} | {color}{prefix} {info}{colorama.Style.RESET_ALL}")


def create_id(length):
    chars = ("abcdefghijklmnopqrstuvwxyz"
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "1234567890-_")
    string = []
    for i in range(length):
        if i == 0 or i == length - 1:
            string.append(random.choice(chars[0:61]))
        else:
            string.append(random.choice(chars))
    return "".join(string)