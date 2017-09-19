 # -*- coding: utf-8 -*-
# filename: Resource.py


#Oliver: Summarize all kinds of language in this class to support Global language msg

import random

class Resource(object):
    #Private
    __MSG = {
        "en" : {
            "WlcMsg" : "Welcome to follow us. You can test the voice recognition feature..",
            #"WlcMsg" : "Thanks for subscribing our channel. We aim to eat everywhere and travel to everywhere you want " \
            #       "without any language specifications. History articles as below. Reply \"View No.\" to check (e.g. View 1)\n----------------\n",
            "Menu" : "The Support Command as below\n------------------\n"
                     "View No. (eg. View 1)\n"
                     "History (eg. History)\n"
                     "Weather City (eg. Weather beijing)\n"
                     "SubWea City (eg. SubWea beijing to monitor BJ weather)\n"
                     "UnsubWea City (eg. UnsubWea beijing)\n",
            "Unidentified": "Invalid command.",
            "ViewCMD" : "Reply \"View No.\" to check (e.g. View 1)\n----------------\n",
            "FirstSub" : "You subscribed <%s> 's weather forecast. Current status: \n",
            "Subbed" : "Subscribed this city %s",
            "SubbedMore" : "Subscribed those cities (%s) weather. New subscribed city status: \n",
            "NoSub": "Haven't subscribed any cities weather",
            "MultiCityError": "Only support to subscribe 1 city weather per request",
            "WeatherHead": "Subscribed below cities weather forecast: ",
            "NoSubCity": "Haven't subscribed any cities weather. Input the city name.",
            "OneCityCheck": "Only support to query 1 city weather per request",
            "SpecifyCity": "Specify the city name",
            "UnSubWea": "Un-subscribed %s 's weather. Current subscribed cities are：%s",
            "UnSubAllWea": "Un-subscribed %s 's weather.No any subscribed cities so far.",
            "WrongCity": "City name wrong. Please check.",
            "OnCitySub": "Only support to un-subscribe 1 city per request",
            "MAXCityLimit" : "Only can subscribe 5 cities weather forecast",
            "UnKnownIssue": "Unknown Issue Happened",
            "NormalHead": "Subscribed cities weather: \n",
            "WrongNum" : "The number is not right.",
            "USay" : "You Said  ",
            "AboutMe" : "I am the clever WeChat Robot and work for HSBC /亲亲",
            "CreateVM": "Applying the EC2 Instance from AWS for you. I will notify you after it's done.",
            "NoPermission": "Sorry. No permission on this operation. Contact Oliver or other Admin.",
            "RMEC2": "Removing your AWS EC2. I will notiry you after it's done",
            "DeletedEC2": "Removed EC2： %s",
            "NoInstance" : "No finding any instances for this user",
        },

        "zh_CN" : {
            "WlcMsg": "欢迎关注并测试语音识别功能",
            #"WlcMsg": "欢迎关注我们。我们会根据你的手机语言推送相关的语言游记，以及文章。" \
            #                 "希望我们可以让旅游和生活没有语言障碍~~" \
            #                 "以下为历史文章，回复“文章 序号”查看\n*****************\n",
            "Menu" : "详细支持的命令格式如下（你也可以对着麦克风喊出如下的命令）："
                     "\n*****************\n"
                     "天气查询 城市名\n"
                     "天气订阅 城市名\n"
                     "取消订阅 城市名\n"
                     "历史文章\n"
                     "文章 序号\n"
                     "段子\n",
            "USay" : "你说的是： ",
            "ViewCMD" : "回复“文章 序号”查看\n*****************\n",
            "WrongTypeMsg" : "暂且不处理该类型消息",
            "Unidentified" : "不能识别你的操作，无效命令",
            #Userhander
            "FirstSub": "您是首次订阅天气，订阅的城市为：%s。 当前天气如下：\n",
            "EmptyMsg" : "记录不能为空",
            "MultiCityError" : "错误：一次只能订阅一个城市",
            "WeatherHead" : "您已订阅了如下城市的天气： ",
            "NoSubCity" :"未订阅任何城市天气, 请指定城市名称",
            "OneCityCheck" : "目前只支持一次查询一个城市的天气",
            "SpecifyCity" : "请指定城市名称",
            "Subbed" : "已订阅该城市：%s",
            "SubbedMore":"您订阅了这些城市的天气：%s。新订阅城市当前天气：\n",
            "UnSubWea" : "已取消订阅%s的天气。新的订阅城市为：%s",
            "UnSubAllWea" : "已取消订阅{0}的天气。现在未订阅任何城市天气",
            "NoSub" : "未订阅任何城市天气",
            "MAXCityLimit" : "最多同时订阅五个城市天气",
            "WrongCity" : "没有该城市，请检查城市名称",
            "OnCitySub" : "目前只支持一次取消一个城市的天气",
            "QualifiedUser" : "你不是对的人，没权限使用记录和提醒功能",
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
            "RecordFmt" : "%s 本月已累计打卡%s天。",
            "BillHealty" : "今天是月末，按约定该结算啦。 %d (打卡天数) * 1RMB = %d",
            #BirthDayHandler
            "Birth" : "生日快乐（我怕我忘了，提前做好了程序）。",
            "MustHappy" : "你必须开心，也必须正确回复！~~o.o~~ 再说句：",
            "IHappy" : "我很开心",
            "AlwaysHappy" : "那就好，要一直好好地开心咯~~ ，这也是我希望的啦o.o （最后一条啦）",
            "ReplyHappy" : "回复“我很开心”（违心也可以）~~",
            "UnSub" : "用户“%s”取消关注",
            "UnKnownIssue" : "未知错误",
            "WrongNum" : "序号错误，请重新回复“文章 序号”",
            "AboutMe": "我是聪明兼美丽与一身的HSBC WeChat Bot /亲亲",
            "CreateVM" : "正在为您创建AWS EC2。创建完成后会微信通知您。",
            "NoPermission" : "无权操作。请联系Oliver申请权限。",
            "RMEC2" : "正在删除您所有的AWS EC2。删除完成后会微信通知您。",
            "DeletedEC2" : "已删除EC2： %s",
            "NoInstance" : "没有该用户的EC2 Instance",

        }
    }

    __BirthWirhes = { 1 : "生日快乐，天天开心。",
                      2 : "生日快乐，明年更美丽。不过我说的是心情，不是外表。",
                      3 : "生日快乐，天天涨停。不过我说的是体重，不是股票。",
                      4 : "生日快乐，越来越。。。蠢。偶尔蠢蠢，可爱~~哈哈哈",
                      5 : "生日快乐，工资涨一块。",
                      6 : "生日快乐，不快乐，不给涨。",
                      7 : "生日快乐，体重来二斤。。",
                      8 : "生日快乐，不过这句我要骂你，怼你，蠢！十条信息随机选。选中这条就是你的命。",
                      9 : "生日快乐，明年从ladyboy走向lady...",
                      10 : "生日快乐，梦到。。。天上飘着最俗。。最有用的钱。。哈哈哈",
                      }

    @staticmethod
    def getMsg(msg_type, language = "zh_CN"):
        return Resource.__MSG[language].get(msg_type, "NoMSG")


    @staticmethod
    def get_random_birth_msg():
        return  Resource.__BirthWirhes.get(random.randint(1, len(Resource.__BirthWirhes)), "生日快乐。短暂，难忘才好~~")
