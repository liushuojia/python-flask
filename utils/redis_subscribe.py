from utils.Redis import *
import time

def cb(message):
    print(message)

def sub():
    Subscribe(["int_channel", "aa"], cb)


if __name__ =="__main__":
    sub()