import threading, time
from time import sleep
from WeatherHandler import WeatherHandler
from WeChatCon import WeChatHandler
from utill import *
from FileHandler import *
import os, codecs

class RootThread(object):
    def __int__(self):
        pass

    def run(self):
        pass

class SleepSecRun(RootThread):
    def __init__(self):
        pass

    @staticmethod
    def run(func_name, *arg):
        while(1):
            pass


class PublisherToSub(RootThread):
    def __init__(self, thread_name = "myThread"):
        pass

    @staticmethod
    def run(argc):
        while (1):
            print("{0} Sending Msg".format(argc))

            if Utill.night_check_time() == -1:
                sleep(60)
                continue

            weather_dir = "/wechat/data/weather/"
            for file in  os.listdir(weather_dir):
                user_name = file.split("_")[0]
                file_handler = codecs.open(weather_dir + file, "r", "utf-8")
                #oHBF6wUHaE4L2yUfhKMBqcrjoi0g
                if  user_name == "oHBF6wR4kUe4KUNtMMN4J0LKXsPE":
                    sub_weather_text = "蠢货专属的天气预报：@_@\n"
                else:
                    sub_weather_text = "您订阅的天气：\n"
                cities = file_handler.readline().split()

                if len(cities) == 0: #in case empty files
                    continue

                for city in cities:
                    weather = WeatherHandler()
                    sub_weather_text += weather.getWeather(city)
                    sub_weather_text += "-------------------\n"

                wechat_con = WeChatHandler()
                # wechat define 2 types sending way"
                # "touser" : sending wit OpenID
                # "towxname" sending with wechat name
                wechat_con.sendMsgToOneAsPreview(sub_weather_text, "touser", user_name)
                #end for to send weather for a person
            #sending per 2 hours
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

    def add_thread(self, func, *argc):
        self.tThreads.append(threading.Thread(target=func, args=argc))

    def remove_thread(self):
        pass

    def run_threads(self):
        for t in self.tThreads:
            t.setDaemon(True)
            t.start()
