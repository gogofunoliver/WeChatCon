import requests
import json

class WeatherHandler(object):
    def __init__(self):
        self.URL="https://api.seniverse.com/v3/weather/now.json?key=%s&location=%s&language=%s&unit=c"
        self.Key="zeyxqofu9p4terje"
        self.language = "en"

    def getWeather(self, city, language = "zh-Hans"):
        #reset language
        if language == "zh_CN":
            self.language = "zh-Hans"
        else:
            self.language = "en"

        url = self.URL % (self.Key, city, self.language)
        ret_str = ""

        r = requests.get(url)
        if r.status_code == 404:
            ret_str = "Failed"
        else:
            print(r.content)
            jason=r.json()
            ret_str = self.parseJason(r.json())
        return ret_str
        #member
        #URL
        #Key

    def parseJason(self, jsont):
        weatherMsg = ""
        if self.language == "zh-Hans":
            weatherMsg = "地点：{0}\n".format(jsont['results'][0]['location']['path'])
            #weatherMsg += "时区：{0}\n".format(jsont['results'][0]['location']['timezone'])
            weatherMsg += "天气：{0}\n".format(jsont['results'][0]['now']['text'])
            weatherMsg += "温度：{0}\n".format(jsont['results'][0]['now']['temperature'])
            #weatherMsg += "体感温度：{0}\n".format(jsont['results'][0]['now']['feels_like'])
            #weatherMsg += "PM2.5：{0}\n".format(jsont['results'][0]['now']['visibility'])
            #weatherMsg += "风向：{0}\n".format(jsont['results'][0]['now']['wind_direction'])
            weatherMsg += "更新时间：{0}\n".format(jsont['results'][0]['last_update'])
        else:
            weatherMsg = "Location: {0}\n".format(jsont['results'][0]['location']['path'])
            weatherMsg += "Weather: {0}\n".format(jsont['results'][0]['now']['text'])
            weatherMsg += "Temperature: {0}\n".format(jsont['results'][0]['now']['temperature'])
            weatherMsg += "Update: {0}\n".format(jsont['results'][0]['last_update'])
        return weatherMsg