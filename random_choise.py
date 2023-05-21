# lib imports
import random
import re

#local import
import settings

def random_choise(text : str) -> str:
    res = re.sub(r"{(.+?)}", lambda x: random.choice(x.group(1).split("|")), text)
    return res
