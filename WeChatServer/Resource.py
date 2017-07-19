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
        "StupidHead" : "嘉玲专属的天气预报：@_@\n",
        "NormalHead" : "您订阅的天气：\n",
        "Recorded" : "已记录",
        "FailRecord" : "记录失败",
        "Removed" : "已删除",
        #HealthyHander
        "GodSub" : "大神打卡成功 O.o o.O ",
        "LingSub" : "嘉玲打卡成功 O.o o.O ",
        "EatTime" : "吃饭时间到，乖乖吃饭去，瓜皮。",
        "WeakTime" : "起床咯，晒屁屁咯，瓜皮。",
        "SleepTime" : "睡觉时间到，乖乖睡觉去，瓜皮。",
        "NapTime" : "午睡时间到，乖乖睡觉去，瓜皮。",
        "FiveMins" : "五分钟内未打卡，已记录。",
        "ReYes" : "请回复“是”打卡。",
        "RecordFmt" : "%s 本月已累计打卡%s天",
        #BirthDayHandler
        "Birth" : "嘉玲，生日快乐（我怕我忘了，提前做好了程序）。",
        "MustHappy" : "你必须开心，也必须正确回复！~~o.o",
        "IHappy" : "我很开心",
        "AlwaysHappy" : "那就一直好好地开心~~ ，这是我希望的o.o",
        "ReplyHappy" : "回复“我很开心”（违心也可以）~~"

    }

    @staticmethod
    def getMsg(msg_type):
        #add  other languages later
        return Resource.__CN_MSG.get(msg_type, "NoMsg")