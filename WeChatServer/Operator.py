from UserHandler import *
from FileHandler import *
from WeatherHandler import WeatherHandler
import receive
import reply
from Resource import *
from TypeDef import TypeDef

class OperationType(object):

    @staticmethod
    def get_operate_function(action):
        actions = {
            TypeDef.OP_Read : Operate.read,
            TypeDef.OP_Write : Operate.write,
            TypeDef.OP_Check : Operate.check,
            TypeDef.OP_Remove : Operate.remove,
            TypeDef.OP_WeatherSub : Operate.subWeather,
            TypeDef.OP_WeatherChk : Operate.checkWeather,
            TypeDef.OP_WeatherUnSub : Operate.unSubWeather,
        }
        return actions.get(action, TypeDef.Undefined)


class Operate(object):
    @staticmethod
    def check(msg, fromUser):
        content = ""
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            note_set = DBHandler().select("SELECT RecoreData,Note from Notepad WHERE Open_ID = '%s'" % fromUser)
            index = 1
            for line in note_set[1]:
                content = content + str(index) + ") " + line[0].strftime("%Y-%m-%d %H:%M:%S") + " " + line[1] + "\n"
                index += 1
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
            if int(DBHandler().insert("INSERT into Notepad VALUES (null, '%s', null, '%s')" % (fromUser, msg))) == 1:
                content = Resource.getMsg("Recorded")
            else:
                content = Resource.getMsg("FailRecord")
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    @staticmethod
    def remove(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            note_set = DBHandler().select("SELECT IND from Notepad WHERE Open_ID = '%s'" % fromUser)
            index = 1
            for line in note_set[1]:
                if msg == str(index):
                    DBHandler().delete("DELETE from Notepad where IND = '%d'" % line[0])
                index += 1
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

