from UserHandler import *
from FileHandler import *
from WeatherHandler import WeatherHandler
import receive
import reply

class OperationType(object):
    Read = 1
    Write = 2
    Check = 3
    Remove = 4
    WeatherSub = 5
    WeatherChk = 6
    WeatherUnSub = 7
    UnDefined = 8

    @staticmethod
    def get_operate_type(action):
        actions = {
            "查询" : OperationType.Read,
            "记录" : OperationType.Write,
            "查询" : OperationType.Check,
            "删除" : OperationType.Remove,
            "天气订阅" : OperationType.WeatherSub,
            "天气查询" : OperationType.WeatherChk,
            "取消订阅" : OperationType.WeatherUnSub
        }
        return actions.get(action, OperationType.UnDefined)

    @staticmethod
    def get_operate_function(action):
        actions = {
            OperationType.Read : Operate.read,
            OperationType.Write : Operate.write,
            OperationType.Check : Operate.check,
            OperationType.Remove : Operate.remove,
            OperationType.WeatherSub : Operate.subWeather,
            OperationType.WeatherChk : Operate.checkWeather,
            OperationType.WeatherUnSub : Operate.unSubWeather,
        }
        return actions.get(action, OperationType.UnDefined)


class Operate(object):
    @staticmethod
    def check(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            content = file_handler.read_all_record()
        else:
            content = "你不是马**或怼她的人，没权限使用记录和提醒功能"
        return content

    @staticmethod
    def  read(msg):
        pass

    @staticmethod
    def write(msg, fromUser):
        user_handler = UserHandler()
        if len(msg.split()) == 0:
            content = "记录不能为空"
        elif (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            file_handler.add_record(msg)
            content = "已记录"
        else:
            content = "你不是马**或怼她的人，没权限使用记录和提醒功能"
        return content

    @staticmethod
    def remove(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            file_handler.remove_record(msg)
            content = "已删除"
        else:
            content = "你不是马**或怼她的人，没权限使用记录和提醒功能"
        return content

    #msg including city
    @staticmethod
    def subWeather(msg, fromUser):
        content = ""
        size_city = len(msg.split())
        if size_city > 1:
            content = "错误：一次只能订阅一个城市"
        elif size_city == 0:
            cities = UserHandler.show_user_sub_city(fromUser)
            if len(cities.split()) != 0:
                content = "您订阅了这些城市的天气：{0}".format(UserHandler.show_user_sub_city(fromUser))
            else:
                content = "未订阅任何城市天气"
        else:
            content = UserHandler.sub_user_for_weather(fromUser, msg)
        return content

    @staticmethod
    def checkWeather(msg, fromUser):
        content = ""
        city_size = len(msg.split())
        if city_size > 1:
            content = "目前只支持一次查询一个城市的天气"
        elif city_size == 0:
            content = "请指定城市名称"
        else:
            weather = WeatherHandler()
            ret = weather.getWeather(msg)
            if ret != "Failed":
                content = ret
            else:
                content = "没有该城市，请检查城市名称"
        return content

    @staticmethod
    def unSubWeather(msg, fromUser):
        city_size = len(msg.split())
        if city_size > 1:
            content = "目前只支持一次取消一个城市的天气"
        elif city_size == 0:
            content = "请指定城市名称"
        else:
            content = UserHandler.unSub_Weahter(fromUser,msg)
        return content

