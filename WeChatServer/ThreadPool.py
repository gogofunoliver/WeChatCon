import threading, time
from time import sleep
from WeatherHandler import WeatherHandler
from WeChatCon import WeChatHandler
from utill import *
from FileHandler import *
import os, codecs
from DBHandler import DBHandler
from Resource import Resource

class RootThread(object):
    def __int__(self):
        pass

    def run(self):
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
            user_sub_result = DBHandler().select("SELECT Open_ID,Cities from WeatherSub")
            for user_sub in user_sub_result[1]:
                user = user_sub[0]
                cities = user_sub[1].split()
                if user == "oHBF6wR4kUe4KUNtMMN4J0LKXsPE":
                    sub_weather_text = Resource.getMsg("StupidHead")
                else:
                    sub_weather_text = Resource.getMsg("NormalHead")

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
                wechat_con.sendMsgToOneAsPreview(sub_weather_text, "touser", user)
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

    def add_thread(self, thread_name, func, *argc):
        self.tThreads.append(threading.Thread(name=thread_name, target=func, args=argc))

    def remove_thread(self):
        pass

    def run_threads(self):
        for t in self.tThreads:
            t.setDaemon(True)
            t.start()
