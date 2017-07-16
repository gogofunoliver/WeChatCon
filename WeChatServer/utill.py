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
        if (local_hour == 23) or (local_hour >= 0 and local_hour < 8):
            print("Night Time, don't send any message")
            ret = -1
        return ret

class Tester(object):
    def test(self, msg):
        print("test : %s" % msg)
        threading.Timer(3,self.test2, ("bbbb",)).start()

    def test2(self, msg2):
        print("test2 : %s" % msg2)

'''
if __name__ == "__main__":
    threading.Timer(3, Tester().test, ("aaa", )).start()
'''