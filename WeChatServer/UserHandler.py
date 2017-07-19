# -*- coding: utf-8 -*-
# filename: UserHandler.py

import codecs, os
from WeatherHandler import WeatherHandler
from FileHandler import FileHandler
from DBHandler import DBHandler
from Resource import  Resource

class UserHandler(object):
    openID = {
        "oHBF6wUHaE4L2yUfhKMBqcrjoi0g": 1, #oliver
        "oHBF6wR4kUe4KUNtMMN4J0LKXsPE": 2, #chun
        "oHBF6wTt-wD22eAwEJLVozjcQjxo": 3, #Jesse
    }

    user_name = {
        "szwlove" : 1,
        "kaarinn" : 2,
        "danny975241564" : 3,
    }

    def __init__(self):
        pass

    @staticmethod
    def verify_user(user):
        if UserHandler.openID.get(user, "NoUser") == "NoUSer":
            print("No Such User {0}".format(user))
            return -1
        else:
            return 0

    @staticmethod
    def add_user(user):
        size = len(UserHandler.openID)
        UserHandler.openID[user] = size + 1

    @staticmethod
    def sub_user_for_weather(user, new_city):
        #QUERY
        user_sub_result = DBHandler().select("SELECT Cities from WeatherSub WHERE Open_ID = '%s'" % user)
        content = ""

        if len(new_city.split()) == 0 and int(user_sub_result[0]) > 0:
            content = Resource.getMsg("WeatherHead") + user_sub_result[1][0][0] #only one cell here, use [0][0] to visit
        elif int(user_sub_result[0]) == 0 and len(new_city.split()) == 0:
            content = Resource.getMsg("NoSubCity")
        #INSERT
        elif int(user_sub_result[0]) == 0 and len(new_city.split()) != 0:
            weather = WeatherHandler()
            ret = weather.getWeather(new_city)
            if ret != "Failed":
                content = "您是首次订阅天气，订阅的城市为：{0}。 当前天气如下：\n".format(new_city) + ret
                # write sub info into db
                insert_sql = "INSERT into WeatherSub VALUES ('%s', '%s', NULL)" % (user, new_city)
                DBHandler().insert(insert_sql)
            else:
                content = "城市名称有误，请修改后，重新订阅"
        #UPDATE
        elif int(user_sub_result[0]) > 0 and len(new_city.split()) != 0:
            old_cities = user_sub_result[1][0][0].split()
            if len(old_cities) > 5:
                content = "最多同时订阅五个城市天气"
            elif new_city in old_cities:
                content = "已订阅该城市：{0}".format(new_city)
            else:
                weather = WeatherHandler()
                ret = weather.getWeather(new_city)
                if ret != "Failed":
                    old_cities.append(new_city)
                    content = "您订阅了这些城市的天气：{0}。新订阅城市当前天气：\n".format(" ".join(old_cities)) + ret
                    update_sql = "UPDATE WeatherSub SET Cities = '%s' WHERE Open_ID = '%s'" % (" ".join(old_cities), user)
                    DBHandler().update(update_sql)
                else:
                    content = "城市名称有误，请修改后，重新订阅"
        else:
            content = "未知错误"
        return content

    @staticmethod
    def unSub_Weahter(user, city):
        # QUERY
        user_sub_result = DBHandler().select("SELECT Cities from WeatherSub WHERE Open_ID = '%s'" % user)
        content = ""
        if int(user_sub_result[0]) > 0:
            old_cities = user_sub_result[1][0][0].split()
            if city not in old_cities:
                content = "未订阅<%s>天气" % city
            else:
                old_cities.remove(city)
                if len(old_cities) > 0:
                    content = "已取消订阅{0}的天气。新的订阅城市为：{1}".format(city, " ".join(old_cities))
                    update_sql = "UPDATE WeatherSub SET Cities = '%s' WHERE Open_ID = '%s'" % (" ".join(old_cities), user)
                    DBHandler().update(update_sql)
                else:
                    content = "已取消订阅{0}的天气。现在未订阅任何城市天气".format(city)
                    delete_sql = "DELETE from WeatherSub WHERE Open_ID = '%s'" % (user)
                    DBHandler().delete(delete_sql)

        else:
            content = "未订阅任何城市天气"
        return content