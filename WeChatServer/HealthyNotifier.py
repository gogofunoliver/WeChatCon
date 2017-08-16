 # -*- coding: utf-8 -*-
# filename: HealthyNotifier.py

import threading, os
from ThreadPool import RootThread
import time
from time import sleep
from FileHandler import FileHandler
from WeChatCon import WeChatHandler
from DBHandler import DBHandler
from Resource import Resource
import logging
from utill import Utill

class HealthyNotifier(RootThread):
    __singleton = None

    @staticmethod
    def get_instance():
        if HealthyNotifier.__singleton is None:
            HealthyNotifier.__singleton = HealthyNotifier("Notifier")
        return HealthyNotifier.__singleton

    def __init__(self, msg):
        self.logger = logging.getLogger("root.HealthyNotifier")
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
            for user in self.user_list:
                ret = WeChatHandler().sendMsgViaCust(msg + Resource.getMsg("ReYes"), "touser", user)
                if int(ret) != 0:
                    print("HealthyNotifier Cust Msg failed..Use preview")
                    WeChatHandler().sendMsgToOneAsPreview(msg + Resource.getMsg("ReYes"), "touser", user)
                self.user_wait_list.append(user)
                threading.Timer(300, self.clear_wait, (user,)).start()

    def clear_wait(self, user_open_id):
        if user_open_id in self.user_wait_list:
            self.user_wait_list.remove(user_open_id)
            ret = WeChatHandler().sendMsgViaCust(Resource.getMsg("FiveMins"), "touser", user_open_id)
            if int(ret) != 0:
                print("HealthyNotifier Cust Msg failed..Use preview")
                WeChatHandler().sendMsgToOneAsPreview(Resource.getMsg("FiveMins"), "touser", user_open_id)
            DBHandler().insert("INSERT into HealthyRecord VALUES (null, '%s', 'N', null)" % user_open_id)
        else:
            #has record into DB when user reply the correct message
            pass

    def check_wait(self, user, msg):
        content = ""
        counts = 0
        if user in self.user_wait_list and user == self.user_list[0] and msg == "是":
            DBHandler().insert("INSERT into HealthyRecord VALUES (null, '%s', 'Y', null)" % user)
            counts = DBHandler().select("SELECT CreateData from HealthyRecord WHERE IsRecord = 'Y' and CreateData > '2017-08' \
            and CreateData < '2017-09' AND Open_ID = '%s'" % user)[0]
            content = Resource.getMsg("RecordFmt") % (Resource.getMsg("GodSub"), str(counts))
            self.user_wait_list.remove(user)
            if Utill.is_last_day():
                content = content + Resource.getMsg("BillHealty") % (counts, counts)
        elif user in self.user_wait_list and user == self.user_list[1] and msg == "是":
            DBHandler().insert("INSERT into HealthyRecord VALUES (null, '%s', 'Y', null)" % user)
            counts = DBHandler().select("SELECT CreateData from HealthyRecord WHERE IsRecord = 'Y' and CreateData > '2017-08' \
            and CreateData < '2017-09' AND Open_ID = '%s'" % user)[0]
            content =  Resource.getMsg("RecordFmt") % (Resource.getMsg("LingSub"), str(counts))
            self.user_wait_list.remove(user)
            if Utill.is_last_day():
                content = content + Resource.getMsg("BillHealty") % (counts, counts)
        return content

    def __meal_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("meal"):
            content = Resource.getMsg("EatTime")
        return content


    def __getup_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("getup"):
            content = Resource.getMsg("WeakTime")
        return  content

    def __sleep_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("sleep"):
            content = Resource.getMsg("SleepTime")
        return content

    def __nap_check(self):
        content = ""
        local_time = time.strftime('%H:%M', time.localtime(time.time()))
        if local_time in self.healthy_metrics.get("nap"):
            content = Resource.getMsg("NapTime")
        return content
