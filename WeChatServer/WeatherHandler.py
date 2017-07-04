import requests
import json

class WeatherHandler(object):
    def __init__(self):
        self.URL="https://api.seniverse.com/v3/weather/now.json"
        self.Key="zeyxqofu9p4terje"

    def getWeather(self, city):
        url = self.URL + '?key=' + self.Key + '&location=' + city + '&language=zh-Hans&unit=c'

        r = requests.get(url)
        print(r.content)
        jason=r.json()
        return self.parseJason(r.json())

        #member
        #URL
        #Key

    def parseJason(self, jsont):
        weatherMsg = "地点：{0}\n".format(jsont['results'][0]['location']['path'])
        #weatherMsg += "时区：{0}\n".format(jsont['results'][0]['location']['timezone'])
        weatherMsg += "天气：{0}\n".format(jsont['results'][0]['now']['text'])
        weatherMsg += "温度：{0}\n".format(jsont['results'][0]['now']['temperature'])
        #weatherMsg += "体感温度：{0}\n".format(jsont['results'][0]['now']['feels_like'])
        #weatherMsg += "PM2.5：{0}\n".format(jsont['results'][0]['now']['visibility'])
        #weatherMsg += "风向：{0}\n".format(jsont['results'][0]['now']['wind_direction'])
        weatherMsg += "更新时间：{0}\n".format(jsont['results'][0]['last_update'])
        return weatherMsg