 # -*- coding: utf-8 -*-
# filename: BirthDayNotifier.py
import time
import threading
from time import sleep
from ThreadPool import RootThread, ThreadPool
from DBHandler import DBHandler
from WeChatCon import WeChatHandler
from Resource import Resource
from ActionHandler import *
import logging

class BirthDayNotifier(RootThread):

    def __del__(self):
        pass

    def __init__(self):
        self.logger = logging.getLogger("root.BirthDayNotifier")

    def run(self, arg):
        today_match = {"": ""}
        while(1):
            all_user_birth = DBHandler().select("SELECT Open_ID,BirthDay from UserInfo")
            for user_line in all_user_birth[1]:
                user_id = user_line[0]
                if user_line[1] is not None:
                    user_birth = user_line[1].strftime("%Y-%m-%d")
                    birth_MM_DD = user_birth.split("-", 1)[1]
                else:
                    birth_MM_DD = ""

                now_MM_DD = time.strftime('%m-%d', time.localtime(time.time()))

                if birth_MM_DD == now_MM_DD and today_match.get(user_id, "NoRecord") != birth_MM_DD:
                    today_match[user_id] = now_MM_DD
                    print("match")
                    ret = WeChatHandler().sendMsgViaCust(Resource.getMsg("Birth") + Resource.getMsg("ReplyHappy"),
                                                         "touser", user_id)
                    if int(ret) != 0:
                        print("BirthDayNotifier Cust Msg failed..Use preview")
                        sleep(300)
                        WeChatHandler().sendMsgToOneAsPreview(Resource.getMsg("Birth") + Resource.getMsg("ReplyHappy"),
                                                       "touser", user_id)

                    ActionsExecutor.add_manual_action(user_id, Action(self.check_reply, user_id, "NoHappy"))
                    threading.Timer(3600, self.get_action, args=(user_id,)).start()
            self.logger.debug("Sleep Birth")
            sleep(120)

    def get_action(self, user):
        self.logger.info("BirthDayNotifier.get_action  timer")
        actions = ActionsExecutor.manual_action_handlers.get(user)
        while type(actions) == list and len(actions) > 0:
            # FIFS
            action = actions.pop(0)
            action.execute_with_arg(user, "No", "Y")
            #action.execute()

        threading.Timer(3600, self.get_action, args=(user,)).start()

    def check_reply(self, user, msg, isTimer='N'):
        reply_msg = ""

        if msg != Resource.getMsg("IHappy"):
            reply_msg = Resource.getMsg("MustHappy") + Resource.get_random_birth_msg()
            ActionsExecutor.add_manual_action(user, Action(self.check_reply, user, "NoHappy"))
        else:
            reply_msg = Resource.getMsg("AlwaysHappy")

        if isTimer == "Y":
            ret = WeChatHandler().sendMsgViaCust(reply_msg, "touser", user)
            if int(ret) != 0:
                print("BirthDayNotifier.get_action  timer")
                WeChatHandler().sendMsgToOneAsPreview(reply_msg, "touser", user)
        self.logger.info("check_reply return %s" % reply_msg)
        return reply_msg