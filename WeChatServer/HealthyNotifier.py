 # -*- coding: utf-8 -*-
# filename: HealthyNotifier.py

import threading, os
from ThreadPool import RootThread
import time
from time import sleep
from FileHandler import FileHandler
from WeChatCon import WeChatHandler
from DBHandler import DBHandler

class HealthyNotifier(RootThread):
    __singleton = None

    @staticmethod
    def get_instance():
        if HealthyNotifier.__singleton is None:
            HealthyNotifier.__singleton = HealthyNotifier("Notifier")
        return HealthyNotifier.__singleton

    def __init__(self, msg):
        self.healthy_metrics = {
            "meal" : ("12:00", "18:40"),
            "sleep" : ("23:30"),
            "nap" : ("13:00"),
            "getup" : ("08:30")
        }
        self.user_list  = [ "oHBF6wUHaE4L2yUfhKMBqcrjoi0g", #oliver
                            "oHBF6wR4kUe4KUNtMMN4J0LKXsPE"  #caroline
        ]
        self.user_wait_list = []
        print("Init HealthyNotifier {0}".format(msg))

    def run(self, *argv):
        while (1):
            print("time : {0}".format(time.strftime('%H:%M', time.localtime(time.time()))))
            self.__notify(self.__sleep_check())
            sleep(60)

    #Private
    def __notify(self, msg):
        if msg != "":
            wechat_con = WeChatHandler()

            for user in self.user_list:
                wechat_con.sendMsgToOneAsPreview(msg + "请回复“是”打卡。", "touser", user)
                self.user_wait_list.append(user)
                threading.Timer(300, self.clear_wait, (user,)).start()

    def clear_wait(self, user_open_id):
        if user_open_id in self.user_wait_list:
            self.user_wait_list.remove(user_open_id)
            WeChatHandler().sendMsgToOneAsPreview("五分钟内未打卡，已记录。", "touser", user_open_id)
            DBHandler().insert("INSERT into HealthyRecord VALUES (null, '%s', '未打卡', null)" % user_open_id)

    def check_wait(self, user, msg):
        content = ""
        if user in self.user_wait_list and user == self.user_list[0] and msg == "是":
            content = "大神打卡成功 O.o o.O"
            self.user_wait_list.remove(user)
        elif user in self.user_wait_list and user == self.user_list[1] and msg == "是":
            content = "蠢货打卡成功 O.o o.O"
            self.user_wait_list.remove(user)
        return content

    def __meal_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("meal"):
            content = "吃饭时间到，乖乖吃饭去，瓜皮。"
        return  content


    def __getup_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("getup"):
            content = "起床咯，晒屁屁咯，瓜皮。"
        return  content

    def __sleep_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("sleep"):
            content = "睡觉时间到，乖乖睡觉去，瓜皮。"
        return content

    def __nap_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("nap"):
            content = "午睡时间到，乖乖睡觉去，瓜皮。"
        return content
