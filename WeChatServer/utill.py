#coding:utf-8
import time
from time import sleep
#from WeChatCon import *
import json
import threading
import os
import logging,logging.config
from TypeDef import TypeDef

class Utill(object):
    @staticmethod
    def night_check_time():
        ret = 0
        local_hour = int(time.strftime('%H', time.localtime(time.time())))
        if (local_hour == 22) or (local_hour == 23) or (local_hour >= 0 and local_hour < 8):
            print("Night Time, don't send any message")
            ret = -1
        return ret

    @staticmethod
    def log_init():
        #init log from the conf file
        logging.config.fileConfig("conf/logging.conf")
        #every py module init it's logger
        #can overwrite the log level in logginf.conf for every log

    @staticmethod
    def create_qr_ticket():
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s"

        QR_data = {
                      "expire_seconds": 604800,
                      "action_name": "QR_STR_SCENE",
                      "action_info":
                          {
                              "scene":
                                  {
                                       "scene_str": "test"
                                  }
                          }
                   }
        token = WeChatHandler().getWeChatToken()
        r = requests.post(url % token, data=json.dumps(QR_data).encode('utf-8'))

    @staticmethod
    def asDigital(digital_str):
        temp_dig = ""
        if digital_str.isdigit():
            return digital_str

        for i in digital_str:
            if i in TypeDef.digital.keys():
                temp = TypeDef.digital[i]
                temp_dig += str(temp)
            else:
                temp_dig = "-1"

        return int(temp_dig)



    @staticmethod
    def is_last_day():
        ret = 0
        lastDays = ["01-31", "0is_last_day3-31", "04-30", "05-31", "06-30", "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
        local_mmdd = time.strftime('%m-%d', time.localtime(time.time()))
        if local_mmdd in lastDays:
            ret = 1
        elif int(time.strftime('%Y', time.localtime(time.time()))) % 4 != 0 and local_mmdd == "2-28":
            ret = 1
        elif int(time.strftime('%Y', time.localtime(time.time()))) % 4 == 0 and local_mmdd == "2-29":
            ret = 1
        else:
            ret = 0
        return ret

class Test1(object):
    __singleton = None

    def __init__(self):
        self.__lock = threading.Lock()

    @staticmethod
    def get_instance():
        if Test1.__singleton is None:
            Test1.__singleton = Test1()
        return Test1.__singleton

    def test1(self):
        self.__lock.acquire()
        print("test1")
        sleep(5)
        print("test1 END")
        self.__lock.release()

    def test2(self):
        self.__lock.acquire()
        print("test2")
        sleep(30)
        print("test2 END")
        self.__lock.release()

class ConText(object):
    context_list = {}

    def __init__(self):
        pass

    @staticmethod
    def add_con(openID, context):
        ConText.context_list[openID] = context
        pass

    @staticmethod
    def rm_con(openID):
        ConText.context_list.pop(openID)
        pass



if __name__ == "__main__":
   from WeChatDownload import BaiduCaller
   import base64, sys, os
   f = open("/tmp/voice.amr", "rb")
   speech = base64.b64encode(f.read())
   str_s = str(speech, encoding="gbk")
   size = os.path.getsize("/tmp/voice.amr")
   BaiduCaller().callBaidu(size, str_s)
   pass