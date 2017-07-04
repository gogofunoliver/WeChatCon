import threading
from time import sleep
from WeatherHandler import WeatherHandler
from WeChatCon import WeChatHandler

class RootThread(object):
    def __int__(self):
        pass

    def run(self):
        pass

class TimerThread(RootThread):
    def __init__(self, thread_name = "myThread"):
        self.__myname__ = thread_name

    def run(self, argc=""):
        while (1):
            print("{0} Sending Msg".format(argc))
            ##get user id
            wechat_con = WeChatHandler()
            wechat_con.sendMsgToOneAsPreview()
            sleep(7200)

class ThreadPool(object):

    __singleton = None

    def __init__(self):
        self.tThreads = []

    @staticmethod
    def get_instance():
        if ThreadPool.__singleton is None:
            ThreadPool.__singleton = ThreadPool()
        return ThreadPool.__singleton

    def add_thread(self, func, argc = ""):
        self.tThreads.append(threading.Thread(target=func, args=(argc,)))

    def remove_thread(self):
        pass

    def run_threads(self):
        for t in self.tThreads:
            t.setDaemon(True)
            t.start()
