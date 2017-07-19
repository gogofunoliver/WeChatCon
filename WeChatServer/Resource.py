 # -*- coding: utf-8 -*-
# filename: Resource.py


#Oliver: Summarize all kinds of language in this class to support Global language msg

class Resource(object):
    #Private
    __CN_MSG = {
        "Menu" : "正确的命令格式如下：\n*****************\n天气查询 城市名\n天气订阅 城市名\n取消订阅 城市名\n",
        "WrongTypeMsg" : "暂且不处理该类型消息",
        "Unidentified" : "不能识别你的操作，无效命令",
        "EmptyMsg" : "记录不能为空",
        "MultiCityError" : "错误：一次只能订阅一个城市",
        "WeatherHead" : "您已订阅了如下城市的天气： ",
        "NoSubCity" :"未订阅任何城市天气, 请指定城市名称",
        "OneCityCheck" : "目前只支持一次查询一个城市的天气",
        "SpecifyCity" : "请指定城市名称",
        "WrongCity" : "没有该城市，请检查城市名称",
        "OnCitySub" : "目前只支持一次取消一个城市的天气",
        "QualifiedUser" : "你不是马**或怼她的人，没权限使用记录和提醒功能",
        "StupidHead" : "蠢货专属的天气预报：@_@\n",
        "NormalHead" : "您订阅的天气：\n",
        "Recorded" : "已记录",
        "FailRecord" : "记录失败",
        "Removed" : "已删除",
        "Birth" : "生日快乐，蠢货（我怕我忘了，提前做好程序，哼）。",
        "MustHappy" : "你必须开心，也必须正确回复！~~o.o",
        "IHappy" : "我很开心",
        "AlwaysHappy" : "那就一直好好地开心~~ ，这是我希望的o.o",
        "ReplyHappy" : "回复“我很开心”（违心也可以）~~"

    }

    @staticmethod
    def getMsg(msg_type):
        #add  other languages later
        return Resource.__CN_MSG.get(msg_type, "NoMsg")