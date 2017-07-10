# -*- coding: utf-8 -*-
# filename: UserHandler.py

import codecs, os
from WeatherHandler import WeatherHandler
from FileHandler import FileHandler

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
    def show_user_sub_city(user):
        record_file = "/wechat/data/weather/" +  user + "_weather.data"
        content = ""
        if os.path.exists(record_file):
            file_handler = codecs.open(record_file, 'r', 'utf-8')
            content = file_handler.readline()
            file_handler.close()
        return content

    @staticmethod
    def sub_user_for_weather(user, new_city):
        first_sub = 0
        record_file = "/wechat/data/weather/" +  user + "_weather.data"
        first_sub = FileHandler.create_file_if_no(record_file)

        file_handler = codecs.open(record_file, 'r', 'utf-8')
        old_cities = file_handler.readline().split()
        file_handler.close()

        if len(old_cities) == 0:
            first_sub = 1

        file_handler = codecs.open(record_file, 'w', 'utf-8')
        content = ""

        if len(new_city.split()) != 0 and new_city not in old_cities:
            weather = WeatherHandler()
            ret = weather.getWeather(new_city)
            if ret != "Failed":
                content = "订阅城市现在的天气：\n" + ret
                old_cities.append(new_city)
                file_handler.write(" ".join(old_cities))
                file_handler.flush()
                if first_sub:
                    content = "您是首次订阅天气，订阅的城市为：{0} \n".format(" ".join(old_cities)) + ret
                else:
                    content = "您订阅了这些城市的天气：{0} \n".format(" ".join(old_cities)) + ret
            else:
                # faile for new city
                file_handler.write(" ".join(old_cities))
                file_handler.flush()
                content = "城市名称有误，请修改后，重新订阅"

        elif new_city in old_cities:
            content = "已订阅该城市：{0}".format(new_city)
            file_handler.write(" ".join(old_cities))
        else:
            pass

        file_handler.close()
        return content

    @staticmethod
    def unSub_Weahter(user, city):
        content = ""
        record_file = "/wechat/data/weather/" + user + "_weather.data"
        if os.path.exists(record_file):
            file_handler = codecs.open(record_file, 'r', 'utf-8')
            cities = file_handler.readline().split()
            file_handler.close()
            if city not in cities:
                content = "未订阅该城市天气"
            else:
                cities.remove(city)
                if len(cities):
                    file_handler = codecs.open(record_file, 'w', 'utf-8')
                    file_handler.write(" ".join(cities))
                    file_handler.close()
                    content = "以取消订阅{0}的天气。新的订阅城市为：{1}".format(city, " ".join(cities))
                else:
                    content = "以取消订阅{0}的天气。现在未订阅任何城市天气".format(city)
        else:
            content = "未订阅任何城市天气"
        return content