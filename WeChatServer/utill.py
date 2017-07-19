import time
from WeChatCon import *
#from ThreadPool import *
import json
import threading

class Utill(object):
    @staticmethod
    def night_check_time():
        ret = 0
        local_hour = int(time.strftime('%H', time.localtime(time.time())))
        if (local_hour == 22) or (local_hour == 23) or (local_hour >= 0 and local_hour < 8):
            print("Night Time, don't send any message")
            ret = -1
        return ret

class Test1(object):
    def __init__(self):
        print("init1")

    def __init__(self, msg):
        print(msg)
