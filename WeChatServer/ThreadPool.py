import threading, time
from time import sleep

import os
import codecs
import logging
from DBHandler import DBHandler
from Resource import Resource
from WeatherHandler import WeatherHandler
from WeChatCon import WeChatHandler
from FileHandler import *
from utill import  Utill


class RootThread(object):
    def __int__(self):
        pass

    def run(self):
        pass

class PublisherToSub(RootThread):
    logger = logging.getLogger("root.ThreadPool")

    def __init__(self, thread_name = "myThread"):
        pass

    @staticmethod
    def run(argc):
        while (1):
            if Utill.night_check_time() == -1 or os.path.exists("/wechat/data/skip_weather"):
                sleep(60)
                continue
            user_sub_result = DBHandler().select("SELECT Open_ID,Cities from WeatherSub")
            for user_sub in user_sub_result[1]:
                user = user_sub[0]
                user_info = WeChatHandler().getUserInfo(user)
                if user_info['subscribe' ] == 0:
                    #User has un-usb our channel
                    continue

                cities = user_sub[1].split()
                if user == "oHBF6wR4kUe4KUNtMMN4J0LKXsPE":
                    sub_weather_text = Resource.getMsg("StupidHead")
                else:
                    sub_weather_text = Resource.getMsg("NormalHead", user_info['language'])

                if len(cities) == 0: #in case empty files
                    continue


                for city in cities:
                    sub_weather_text += WeatherHandler().getWeather(city, user_info['language'])
                    sub_weather_text += "-------------------\n"

                # wechat define 2 types sending way"
                # "touser" : sending wit OpenID
                # "towxname" sending with wechat name
                WeChatHandler().sendMsgToOneAsPreview(sub_weather_text, "touser", user)
                PublisherToSub.logger.info("Sent weather to %s. Weather: %s" % (user, sub_weather_text))
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
