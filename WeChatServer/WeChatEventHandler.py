import json
from TypeDef import TypeDef
from DBHandler import DBHandler
from WeChatCon import WeChatHandler
from UserHandler import UserHandler
from Resource import  Resource
#from CloudVision import GCPCV
import threading
from ActionHandler import *
from time import sleep
from Operator import Operate

class WeChatEventHanlder(Operate):
    @staticmethod
    def refreshUser():
        all_user = WeChatHandler().getAllUserOpenID()

        for open_ID in all_user['data']['openid']:
            WeChatEventHanlder.onSub(open_ID)

    @staticmethod
    def onSub(user_open_ID):
        user_dict = WeChatHandler().getUserInfo(user_open_ID)
        user_priority = UserHandler.verify_user(user_open_ID)
        if user_priority == -1:
            user_insert_sql = "INSERT into UserInfo VALUES ('%s', 'N', '%s', null, '%s', null, null, null, '%s', null, " \
                              "null, null, null)" % (
                              user_open_ID, user_dict['nickname'], TypeDef.sex_dict[user_dict['sex']],
                              (user_dict['city'] + ',' + user_dict['province'] + ',' + user_dict[
                                  'country']).replace("\'", "\\\'"))
            DBHandler().insert(user_insert_sql)
        else:
            update_sql = "UPDATE UserInfo SET WechatName = '%s',Sex='%s',Address='%s' WHERE Open_ID = '%s'"\
                         %  (user_dict['nickname'], TypeDef.sex_dict[user_dict['sex']],
                         (user_dict['city'] + ',' + user_dict['province'] + ',' + user_dict['country']).replace("\'", "\\\'"),
                            user_open_ID)
            DBHandler().update(update_sql)

        return_msg = Resource.getMsg("WlcMsg", user_dict['language'])
        '''
        if user_dict['language'] == "zh_CN":
            sql_query = "Select IDX,Media_ID,Title from HistoryArticle"
        else:
            sql_query = "Select IDX,Media_ID,Title from HistoryArticle WHERE Language = 'en'"
        results = DBHandler().select(sql_query)

        for line in results[1]:
            return_msg = return_msg + str(line[0]) + "..." + line[2] + "\n"

        threading.Timer(3, WeChatHandler().sendMsgViaCust,
                        (Resource.getMsg("Menu", user_dict['language']), "touser", user_open_ID)
                        ).start()
       '''
        return return_msg

    @staticmethod
    def onUnSub(user_open_ID):
        WeChatName = DBHandler().select("SELECT WechatName from UserInfo WHERE Open_ID = '%s'" % user_open_ID)[1][0][0]
        if len(WeChatName) > 0:
            msg = Resource.getMsg("UnSub") % WeChatName
        else:
            msg = Resource.getMsg("UnSub") % user_open_ID

        ret = WeChatHandler().sendMsgViaCust(msg)
        if int(ret) != 0:
            print("onUnSub Cust Msg failed..Use preview")
            WeChatHandler().sendMsgToOneAsPreview(msg)
        return "No Action"

    @staticmethod
    def onFoody(user_open_ID):
        return "No Food to eat..."

    @staticmethod
    def onJokeByClick(user_open_ID):
        return WeChatEventHanlder.onJoke("", user_open_ID, "en")

    @staticmethod
    def onTravel(user_open_ID):
        return "I don't know where you want to go"

    @staticmethod
    def onMaEat(user_open_ID):
        return "吃吃吃"

    @staticmethod
    def onMaSleep(user_open_ID):
        return "睡睡睡"

    @staticmethod
    def listHistoryArticleByClick(user_open_ID):
        user_dict = WeChatHandler().getUserInfo(user_open_ID)
        return WeChatEventHanlder.listHistoryArticle("", user_open_ID, user_dict['language'])

    @staticmethod
    def queryHistryAWSAlert(user_open_ID):
        db_rows = DBHandler().select("Select Message from AWS_Record")
        reply_content = ""

        for row in db_rows[1]:
            reply_content = reply_content + row[0] + "\n***************************\n"
        return reply_content

    @staticmethod
    def onCreateVMByClick(user_open_ID):
        user_dict = WeChatHandler().getUserInfo(user_open_ID)
        lang = user_dict['language']
        return WeChatEventHanlder.onCreateVM("", user_open_ID, lang)

    @staticmethod
    def onRemoveVMByClick(user_open_ID):
        user_dict = WeChatHandler().getUserInfo(user_open_ID)
        lang = user_dict['language']
        return WeChatEventHanlder.onDeleteVM("", user_open_ID, lang)

    @staticmethod
    def showAboutMe(user_open_ID):
        user_dict = WeChatHandler().getUserInfo(user_open_ID)
        lang = user_dict['language']
        return Resource.getMsg("AboutMe", lang)

    @staticmethod
    def onSetZH(user_open_ID):
        TypeDef.LANG = TypeDef.Event_SetZH
        return "设置中文"

    @staticmethod
    def onSetEN(user_open_ID):
        TypeDef.LANG = TypeDef.Event_SetEN
        return "Set English"

    @staticmethod
    def onSetCT(user_open_ID):
        TypeDef.LANG = TypeDef.Event_SetCT
        return "Set Cantonese"



class EventRouter(object):
    __sys_event = { TypeDef.Event_SUB : WeChatEventHanlder.onSub,
                    TypeDef.Event_UnSub : WeChatEventHanlder.onUnSub,
    }

    __self_func = {TypeDef.Event_Foody: WeChatEventHanlder.onFoody,
                 TypeDef.Event_Tavel: WeChatEventHanlder.onTravel,
                 TypeDef.Event_Ma_Eat: WeChatEventHanlder.onMaEat,
                 TypeDef.Event_Ma_Sleep: WeChatEventHanlder.onMaSleep,
                 TypeDef.Event_Ma_Joke: WeChatEventHanlder.onJokeByClick,
                 TypeDef.Event_History: WeChatEventHanlder.listHistoryArticleByClick,
                 TypeDef.Event_HistoryAlert : WeChatEventHanlder.queryHistryAWSAlert,
                 TypeDef.Event_ApplyVM : WeChatEventHanlder.onCreateVMByClick,
                 TypeDef.Event_About_Me : WeChatEventHanlder.showAboutMe,
                 TypeDef.Event_RemoveVM : WeChatEventHanlder.onRemoveVMByClick,
                 TypeDef.Event_SetEN : WeChatEventHanlder.onSetEN,
                 TypeDef.Event_SetZH : WeChatEventHanlder.onSetZH,
                 TypeDef.Event_SetCT: WeChatEventHanlder.onSetCT,
    }

    @staticmethod
    def get_envent_func(event, key_value):
        func = ""
        if event in TypeDef.SystemEvent:
            func = EventRouter.__sys_event.get(event, TypeDef.Undefined)
        elif event in TypeDef.CustEvent:
            func = EventRouter.__self_func.get(key_value, EventRouter.undefined_event)
        return func

    @staticmethod
    def upload_image_to_wechat(event, key_value):
        func = ""
        if event in TypeDef.SystemEvent:
            func = EventRouter.__sys_event.get(event, TypeDef.Undefined)
        elif event in TypeDef.CustEvent:
            func = EventRouter.__self_func.get(key_value, EventRouter.undefined_event)
        return func

    @staticmethod
    def undefined_event(open_ID):
        return TypeDef.Undefined


