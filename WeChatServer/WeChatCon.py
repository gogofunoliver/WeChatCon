import requests
import json
import time
from time import sleep
import threading

from WeatherHandler import WeatherHandler

class WechatRefresher(object):
    def __init__(self):
        pass

    @staticmethod
    def start():
        wechat_con = WeChatHandler()
        sleep_time = int(wechat_con.getWeChatToken("true")) - 100
        timer = threading.Timer(sleep_time, WechatRefresher.start)
        timer.start()

class WeChatHandler(object):
    def __init__(self):
        self.appID = "wx3efb6e041b52017b"
        self.secrect = "cd937c454a10339fab500e5e093d63b8"
        self.weChatToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
        self.weChatPreview = "https://api.weixin.qq.com/cgi-bin/message/mass/preview"
        self.token_file = "/wechat/data/token/token_file.data"
        self.custSend = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token="

        self.jsonTextInputTep = '{ \
                "@@TYPE@@": "@@USER@@", \
                 "text": { \
                          "content":"@@MSG@@" \
                          }, \
                 "msgtype": "text" \
                }'

    def getWeChatToken(self, refresh = "false"):
        if refresh == "true":
            url = self.weChatToken + "&appid=" + self.appID + "&secret=" + self.secrect
            weChatTokenJ = requests.get(url)
            print(weChatTokenJ.content)
            #weChatTokenJ="kUZExF2MAWEragNE0VH_4VDcYrPkAWimc_I2jRFaoOmX5jNdPZSzYwUz0ynt1Wnwh-taWFDsAbCeMrTiAvwLFqzZiY6_2ci84xLWT7Uuh84pDI0ulXBRujqmXKw-lIAVOQVdABAVXC"

            if (weChatTokenJ.status_code == 200):
                token = weChatTokenJ.json()["access_token"]
                experied_sec = weChatTokenJ.json()["expires_in"]
                local_time = time.strftime('%Y-%m-%d#@#%H:%M:%S', time.localtime(time.time()))
                print("{0} : Refresh WeChat token: {1}".format(local_time, token))
                token_file = open(self.token_file, "w");
                token_file.write(token.strip())
                token_file.close()
                return  experied_sec
            else:
                print("Error: Cannot get token")
                return 60
        else:
            token_file = open(self.token_file, "r");
            token = token_file.readline().strip()
            token_file.close()
            print("Sucess: get token {0}".format(token))
            return token

    #send to a WeChat user to preview the an article or a msg
    def sendMsgToOneAsPreview(self, msg, type="towxname", to_user="szwlove"):
        token = self.getWeChatToken()
        previewURL = self.weChatPreview + "?access_token=" + token
        status = ""
        ret = 0
        if type == "towxname":
            postInput = self.jsonTextInputTep.replace("@@TYPE@@", type)
            postInput = self.jsonTextInputTep.replace("@@USER@@", to_user)
            postInput = postInput.replace("@@MSG@@", msg)
            r = requests.post(previewURL, data=postInput.encode("utf-8"))
            status = r.content
            ret = r.json()['errcode']
        elif type == "touser":
            postInput = self.jsonTextInputTep.replace("@@TYPE@@", type)
            postInput = postInput.replace("@@USER@@", to_user)
            postInput = postInput.replace("@@MSG@@", msg)
            r = requests.post(previewURL, data=postInput.encode("utf-8"))
            status = r.content
            ret = r.json()['errcode']
        print(status)
        return ret


    #send to a WeChat user to preview the an article or a msg
    def sendMsgViaCust(self, msg, type="towxname", to_user="szwlove"):
        token = self.getWeChatToken()
        sending_url = self.custSend + token
        status = ""
        ret = 0
        if type == "towxname":
            postInput = self.jsonTextInputTep.replace("@@TYPE@@", type)
            postInput = self.jsonTextInputTep.replace("@@USER@@", to_user)
            postInput = postInput.replace("@@MSG@@", msg)
            r = requests.post(sending_url, data=postInput.encode("utf-8"))
            status = r.content
            ret = r.json()['errcode']
        elif type == "touser":
            postInput = self.jsonTextInputTep.replace("@@TYPE@@", type)
            postInput = postInput.replace("@@USER@@", to_user)
            postInput = postInput.replace("@@MSG@@", msg)
            r = requests.post(sending_url, data=postInput.encode("utf-8"))
            status = r.content
            ret = r.json()['errcode']
        print(status)
        return ret


    #send MSG to dedicated group with ID
    def send2Group(self, groupID):
        pass

    def send2All(self):
        pass