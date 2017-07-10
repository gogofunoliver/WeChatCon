import time
from WeChatCon import *
from ThreadPool import *

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
    def __init__(self):
        pass

    @staticmethod
    def test():
        print("test")
'''
if __name__ == "__main__":
    ThreadPool.get_instance().add_thread(PublisherToSub.run, "Publiser")
    ThreadPool.get_instance().run_threads()
'''