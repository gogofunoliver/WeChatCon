# -*- coding: utf-8 -*-
# filename: UserHandler.py

import codecs, os
from WeatherHandler import WeatherHandler
from FileHandler import FileHandler
from DBHandler import DBHandler
from Resource import  Resource
from WeChatCon import WeChatHandler
import logging

class UserHandler(object):
    logger = logging.getLogger("root.UserHandler")

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


    #0 existed and VIP
    #1 existed Non-vip
    #-1 No existed
    @staticmethod
    def verify_user(user):
        ret = -1
        result = DBHandler().select("SELECT VIP from UserInfo where Open_ID = '%s'" % user)
        if int(result[0]) == 1 and result[1][0][0] == 'Y':
            UserHandler.logger.info("Qualified user : %s" % user)
            ret = 0
        elif int(result[0]) == 1 and result[1][0][0] == 'N':
            #existed non-vip
            ret = 1
        else:
            ret = -1
        return ret

    @staticmethod
    def add_user(user):
        size = len(UserHandler.openID)
        UserHandler.openID[user] = size + 1

    @staticmethod
    def user_check_weather(user, city, lang):
        UserHandler.logger.info("User <%s> is checking the city <%s> weather" % (user, city))
        content = ""
        ret = WeatherHandler().getWeather(city, lang)
        if ret != "Failed":
            content = ret
        else:
            content = Resource.getMsg("WrongCity", lang)
        return content

    @staticmethod
    def sub_user_for_weather(user, new_city, lang):
        UserHandler.logger.info("User <%s> is subscribing the city <%s> weather" % (user, new_city))
        #QUERY
        user_sub_result = DBHandler().select("SELECT Cities from WeatherSub WHERE Open_ID = '%s'" % user)
        content = ""

        if len(new_city.split()) == 0 and int(user_sub_result[0]) > 0:
            content = Resource.getMsg("WeatherHead", lang) + user_sub_result[1][0][0] #only one cell here, use [0][0] to visit
        elif int(user_sub_result[0]) == 0 and len(new_city.split()) == 0:
            content = Resource.getMsg("NoSubCity", lang)
        #INSERT
        elif int(user_sub_result[0]) == 0 and len(new_city.split()) != 0:
            weather = WeatherHandler()
            ret = weather.getWeather(new_city, lang)
            if ret != "Failed":
                content = Resource.getMsg("FirstSub", lang) % new_city + ret
                # write sub info into db
                insert_sql = "INSERT into WeatherSub VALUES ('%s', '%s', NULL)" % (user, new_city)
                DBHandler().insert(insert_sql)
            else:
                content = Resource.getMsg("WrongCity", lang)
        #UPDATE
        elif int(user_sub_result[0]) > 0 and len(new_city.split()) != 0:
            old_cities = user_sub_result[1][0][0].split()
            if len(old_cities) > 5:
                content = Resource.getMsg("MAXCityLimit", lang)
            elif new_city in old_cities:
                content = Resource.getMsg("Subbed", lang) % new_city
            else:
                weather = WeatherHandler()
                ret = weather.getWeather(new_city, WeChatHandler().getUserInfo(user)['language'])
                if ret != "Failed":
                    old_cities.append(new_city)
                    content = Resource.getMsg("SubbedMore", lang) % " ".join(old_cities) + ret
                    update_sql = "UPDATE WeatherSub SET Cities = '%s' WHERE Open_ID = '%s'" % (" ".join(old_cities), user)
                    DBHandler().update(update_sql)
                else:
                    content = Resource.getMsg("WrongCity", lang)
        else:
            content = Resource.getMsg("UnKnownIssue", lang)
        return content

    @staticmethod
    def unSub_Weahter(user, city, lang):
        UserHandler.logger.info("User <%s> is un-subscribing the city <%s> weather" % (user, city))
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
                    content = Resource.getMsg("UnSubWea", lang) % (city, " ".join(old_cities))
                    update_sql = "UPDATE WeatherSub SET Cities = '%s' WHERE Open_ID = '%s'" % (" ".join(old_cities), user)
                    DBHandler().update(update_sql)
                else:
                    content = Resource.getMsg("UnSubAllWea", lang) % city
                    delete_sql = "DELETE from WeatherSub WHERE Open_ID = '%s'" % (user)
                    DBHandler().delete(delete_sql)

        else:
            content = Resource.getMsg("NoSub", lang)
        return content
