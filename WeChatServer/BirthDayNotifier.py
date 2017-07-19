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

class BirthDayNotifier (RootThread):
    def __del__(self):
        pass

    def __int__(self):
        self.today_match = {"test": "test"}

    def run(self, arg):
        today_match = {"": ""}
        while(1):
            print(arg)
            #all_user_birth = ("", "")
            all_user_birth = DBHandler().select("SELECT Open_ID,BirthDay from UserInfo")
            for user_line in all_user_birth[1]:
                user_id = user_line[0]
                user_birth = user_line[1].strftime("%Y-%m-%d")
                birth_MM_DD = user_birth.split("-", 1) [1]
                now_MM_DD = time.strftime('%m-%d', time.localtime(time.time()))

                if birth_MM_DD == now_MM_DD and today_match.get(user_id, "NoRecord") != birth_MM_DD:
                    today_match[user_id] = now_MM_DD
                    print("match")
                    WeChatHandler().sendMsgViaCust(Resource.getMsg("Birth") + Resource.getMsg("ReplyHappy"), "touser", user_id)
                    ActionsExecutor.add_manual_action(user_id, Action(self.check_reply, user_id, "NoHappy"))
                    threading.Timer(300, self.get_action, args=(user_id,)).start()
            print("Sleep Birth\n")
            sleep(120)

    def get_action(self, user):
        print("BirthDayNotifier.get_action  timer")
        actions = ActionsExecutor.manual_action_handlers.get(user)
        while type(actions) == list and len(actions) > 0:
            # FIFS
            action = actions.pop(0)
            action.execute()

        threading.Timer(300, self.get_action, args=(user,)).start()

    def check_reply(self, user, msg):
        if msg != Resource.getMsg("IHappy"):
            WeChatHandler().sendMsgViaCust(Resource.getMsg("MustHappy"), "touser", user)
            ActionsExecutor.add_manual_action(user, Action(self.check_reply, user, "NoHappy"))
        else:
            WeChatHandler().sendMsgViaCust(Resource.getMsg("AlwaysHappy"), "touser", user)

def test(msg, msg1):
    print("%s %s " % (msg, msg1))

if __name__ == "__main__":
   func = test
   arg = ("a", "b")
   func(*arg)
