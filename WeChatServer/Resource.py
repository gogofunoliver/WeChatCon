 # -*- coding: utf-8 -*-
# filename: Resource.py


#Oliver: Summarize all kinds of language in this class to support Global language msg

class Resource(object):
    CN_MSG = {
        "Menu" : "正确的命令格式如下：\n*****************\n气查询 城市名\n天气预定 城市名\n取消预定 城市名\n",
        "WrongTypeMsg" : "暂且不处理该类型消息",
        "Unidentified" : "不能识别你的操作，无效命令",
        "EmptyMsg" : "记录不能为空",
        "MultiCityError" : "错误：一次只能订阅一个城市",
        "WeatherHead" : "您订阅了这些城市的天气： ",
        "NoSubCity" :"未订阅任何城市天气",
        "OneCityCheck" : "目前只支持一次查询一个城市的天气",
        "SpecifyCity" : "请指定城市名称",
        "WrongCity" : "没有该城市，请检查城市名称",
        "OnCitySub" : "目前只支持一次取消一个城市的天气",
        "QualifiedUser" : "你不是马**或怼她的人，没权限使用记录和提醒功能",
        "Recorded" : "已记录",
        "Removed" : "已删除",

    }

    @staticmethod
    def getMsg(msg_type):
        #add  other languages later
        return Resource.CN_MSG.get(msg_type, "NoMsg")