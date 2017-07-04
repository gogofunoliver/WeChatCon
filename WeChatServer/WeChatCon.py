import requests
import json
import time

from WeatherHandler import WeatherHandler

class WeChatHandler(object):
    def __init__(self):
        self.appID = "wx3efb6e041b52017b"
        self.secrect = "cd937c454a10339fab500e5e093d63b8"
        self.weChatToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
        self.weChatPreview = "https://api.weixin.qq.com/cgi-bin/message/mass/preview"

        self.jsonTextInputTep = '{ \
                "towxname": "@@USER@@", \
                 "text": { \
                          "content":"@@MSG@@" \
                          }, \
                 "msgtype": "text" \
                }'

    def getWeChatToken(self):
        url = self.weChatToken + "&appid=" + self.appID + "&secret=" + self.secrect
        weChatTokenJ = requests.get(url)
        print(weChatTokenJ.content)
        #weChatTokenJ="kUZExF2MAWEragNE0VH_4VDcYrPkAWimc_I2jRFaoOmX5jNdPZSzYwUz0ynt1Wnwh-taWFDsAbCeMrTiAvwLFqzZiY6_2ci84xLWT7Uuh84pDI0ulXBRujqmXKw-lIAVOQVdABAVXC"

        if (weChatTokenJ.status_code == 200):
            token = weChatTokenJ.json()["access_token"]
            print("WeChat token: {0}".format(token))
            return token
        else:
            print("Cannot get token")


    def formatMsg(self):
        wetherFomater = WeatherHandler()
        sendMsg = "蠢货的专属天气预报 @-@：\n"
        sendMsg += "---------------------------\n"
        sendMsg += wetherFomater.getWeather("guangzhou")
        sendMsg += "---------------------------\n"
        sendMsg += wetherFomater.getWeather("xian")
        return sendMsg

    #send to a WeChat user to preview the an article or a msg
    def sendMsgToOneAsPreview(self, weChatName = "szwlove"):
        if self.check_time() == 0:
            token = self.getWeChatToken()
            previewURL = self.weChatPreview + "?access_token=" + token
            postInput = self.jsonTextInputTep.replace("@@USER@@", weChatName)
            postInput = postInput.replace("@@MSG@@", self.formatMsg())
            r = requests.post(previewURL, data=postInput.encode("utf-8"))
            if (r.status_code != 200):
                print ("error!")
            print(r.content)

    #get The Group ID by name    def getGoupIDByName(self, name):
        pass

    #send MSG to dedicated group with ID
    def send2Group(self, groupID):
        pass

    def send2All(self):
        pass

    def check_time(self):
        ret = 0
        local_hour = int(time.strftime('%H', time.localtime(time.time())))
        if (local_hour == 23) or (local_hour >= 0 and local_hour < 8):
            print("Night Time, don't send any message")
            ret =  -1
        return ret
