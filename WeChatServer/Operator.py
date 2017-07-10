from UserHandler import *
from FileHandler import *
from WeatherHandler import WeatherHandler
import receive
import reply
from Resource import *

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
            content = Resource.getMsg("QualifiedUser")
        return content

    @staticmethod
    def  read(msg):
        pass

    @staticmethod
    def write(msg, fromUser):
        user_handler = UserHandler()
        if len(msg.split()) == 0:
            content = Resource.getMsg("EmptyMsg")
        elif (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            file_handler.add_record(msg)
            content = Resource.getMsg("Recorded")
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    @staticmethod
    def remove(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            file_handler.remove_record(msg)
            content = Resource.getMsg("Removed")
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    #msg including city
    @staticmethod
    def subWeather(msg, fromUser):
        content = ""
        size_city = len(msg.split())
        if size_city > 1:
            content = Resource.getMsg("MultiCityError")
        elif size_city == 0:
            cities = UserHandler.show_user_sub_city(fromUser)
            if len(cities.split()) != 0:
                content = "{0} {1}".format(Resource.getMsg("WeatherHead"), UserHandler.show_user_sub_city(fromUser))
            else:
                content = Resource.getMsg("NoSubCity")
        else:
            content = UserHandler.sub_user_for_weather(fromUser, msg)
        return content

    @staticmethod
    def checkWeather(msg, fromUser):
        content = ""
        city_size = len(msg.split())
        if city_size > 1:
            content = Resource.getMsg("OneCityCheck")
        elif city_size == 0:
            content = Resource.getMsg("SpecifyCity")
        else:
            weather = WeatherHandler()
            ret = weather.getWeather(msg)
            if ret != "Failed":
                content = ret
            else:
                content = Resource.getMsg("WrongCity")
        return content

    @staticmethod
    def unSubWeather(msg, fromUser):
        city_size = len(msg.split())
        if city_size > 1:
            content = Resource.getMsg("OnCitySub")
        elif city_size == 0:
            content = Resource.getMsg("SpecifyCity")
        else:
            content = UserHandler.unSub_Weahter(fromUser,msg)
        return content

