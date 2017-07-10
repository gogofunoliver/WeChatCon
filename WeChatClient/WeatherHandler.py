import requests
import json

from WechatHandler import WeChatHandler

def lambda_handler(event, context):
    wechatCon = WeChatHandler()
    wechatCon.sendMsgToOneAsPreview()

class WeatherHandler(object):
    def __init__(self):
        self.URL="https://api.seniverse.com/v3/weather/now.json"
        self.Key="zeyxqofu9p4terje"

    def getWeather(self, City):
        url = self.URL + '?key=' + self.Key + '&location=' + City + '&language=zh-Hans&unit=c'

        r = requests.get(url)    # 最基本的GET请求
        #print(r.status_code)    # 获取返回状态
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
        weatherMsg += "体感温度：{0}\n".format(jsont['results'][0]['now']['feels_like'])
        #weatherMsg += "PM2.5：{0}\n".format(jsont['results'][0]['now']['visibility'])
        #weatherMsg += "风向：{0}\n".format(jsont['results'][0]['now']['wind_direction'])
        weatherMsg += "更新时间：{0}\n".format(jsont['results'][0]['last_update'])
        return weatherMsg


#if __name__ == '__main__':
#    lambda_handler("a", "b")