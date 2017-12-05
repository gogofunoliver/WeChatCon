import requests
import json
import time
from time import sleep
import threading
import logging
import traceback

from WeatherHandler import WeatherHandler
from DBHandler import DBHandler

class WechatRefresher(object):
    def __init__(self):
        pass

    @staticmethod
    def start():
        wechat_con = WeChatHandler()
        sleep_time = int(wechat_con.getWeChatToken("true")) - 100
        threading.Timer(sleep_time, WechatRefresher.start).start()

class WeChatHandler(object):
    def __init__(self):
        self.logger = logging.getLogger("root.WeChatCon")
        self.appID = "wx3efb6e041b52017b"
        self.secrect = "cd937c454a10339fab500e5e093d63b8"
        self.weChatToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
        self.weChatPreview = "https://api.weixin.qq.com/cgi-bin/message/mass/preview"
        self.token_file = "/wechat/data/token/token_file.data"
        self.custSend = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token="
        self.userInfo = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=en"
        self.allUesr = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s"
        self.getAllNews = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s"
        self.downLoadVoiceUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"
        self.uploadVoiceUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=voice"
        self.uploadImageUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image"
        self.downLoadIMGUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

        self.jsonTextInputTep = '{ \
                "@@TYPE@@": "@@USER@@", \
                 "text": { \
                          "content":"@@MSG@@" \
                          }, \
                 "msgtype": "text" \
                }'

    def getUserInfo(self, user_open_ID):
        token = self.getWeChatToken()
        requst_url = self.userInfo % (token, user_open_ID)
        weChatTokenJ = requests.get(requst_url)
        if weChatTokenJ.status_code == 200:
            return weChatTokenJ.json()
        pass

    def getAllUserOpenID(self):
        token = self.getWeChatToken()
        Tx_return = requests.get(self.allUesr % token)
        return Tx_return.json()

    def getAllNewsIntoDB(self):
        input_jason = { "type":"news",
                        "offset":0,
                        "count":20, }

        req_url = self.getAllNews % self.getWeChatToken()
        Tx_return = requests.post(req_url, data=json.dumps(input_jason).encode('utf-8'))
        Tx_return.encoding = 'utf-8'
        all_news = Tx_return.json()['item']
        for news in all_news:
            if DBHandler().select("SELECT Title from HistoryArticle WHERE Media_ID = '%s'" % news['media_id'])[0] == 0:
                detail = news['content']['news_item'][0] #multi-article in 1 post
                sql = "INSERT into HistoryArticle VALUES (null, '%s', 'zh_CN', '%s', '%s', '%s', null)" \
                      % (news['media_id'], detail['title'].replace("\'", "\\\'"), detail['url'],
                         time.strftime("%Y-%m-%d %X", time.localtime(news['update_time'])))
                self.logger.info("Execute sql: %s" % sql)
                DBHandler().insert(sql)

    def postNewsToUser(self, open_ID, media_ID):
        json_input = {
            "touser": open_ID,
            "msgtype": "mpnews",
            "mpnews":
                {
                    "media_id": media_ID
                }
        }

        r = requests.post(self.custSend + self.getWeChatToken(), data=json.dumps(json_input).encode("utf-8"))
        status = r.content
        ret = r.json()['errcode']
        self.logger.info("Sent to <%s> news. Status: <%s>, <%s>" % (open_ID, ret, status))


    def getWeChatToken(self, refresh = "false"):
        if refresh == "true":
            url = self.weChatToken + "&appid=" + self.appID + "&secret=" + self.secrect
            weChatTokenJ = requests.get(url)
            self.logger.info(weChatTokenJ.content)
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
            self.logger.info("Sucess: get token {0}".format(token))
            return token

    #send to a WeChat user to preview the an article or a msg
    def sendMsgToOneAsPreview(self, msg, type="towxname", to_user="szwlove"):
        token = self.getWeChatToken()
        previewURL = self.weChatPreview + "?access_token=" + token
        status = ""
        ret = 0
        if type == "towxname":
            postInput = self.jsonTextInputTep.replace("@@TYPE@@", type)
            postInput = postInput.replace("@@USER@@", to_user)
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
        self.logger.info("Sent to : %s. Msg : %s. Status: <%s>, <%s>" % (to_user, msg, ret, status))
        print(status)
        return ret


    #send to a WeChat user to preview the an article or a msg
    def sendMsgViaCust(self, msg, type="towxname", to_user="szwlove"):
        wechatInput = {
            "touser": to_user,
            "text": {
                "content": msg,
            },
            "msgtype": "text",
        }
        token = self.getWeChatToken()
        sending_url = self.custSend + token
        r = requests.post(sending_url, data=json.dumps(wechatInput, ensure_ascii=False).encode("utf-8"))
        status = r.content
        ret = r.json()['errcode']
        self.logger.info("Sent to : %s. Msg : %s. Status: <%s>, <%s>" % (to_user, msg, ret, status))
        print(status)
        return ret

    def sendVoiceMsgCust(self, mediaID, openID = "szwlove"):
        wechatInput = {
            "touser": openID,
            "msgtype": "voice",
            "voice":
                {
                    "media_id": mediaID
                }
        }

        token = self.getWeChatToken()
        sending_url = self.custSend + token
        r = requests.post(sending_url, data=json.dumps(wechatInput, ensure_ascii=False).encode("utf-8"))
        status = r.content
        ret = r.json()['errcode']
        self.logger.info("Sent to : %s. Msg : %s. Status: <%s>, <%s>" % (openID, mediaID, ret, status))
        print(status)
        return ret

    def sendImageMsgCust(self, mediaID, openID="szwlove"):
        wechatInput = {
            "touser": openID,
            "msgtype": "image",
            "image":
                {
                    "media_id": mediaID
                }
        }

        token = self.getWeChatToken()
        sending_url = self.custSend + token
        r = requests.post(sending_url, data=json.dumps(wechatInput, ensure_ascii=False).encode("utf-8"))
        status = r.content
        ret = r.json()['errcode']
        self.logger.info("Sent to : %s. Msg : %s. Status: <%s>, <%s>" % (openID, mediaID, ret, status))
        print(status)
        return ret

    def downloadVoiceAsFile(self, mediaID, saveFile):
        token = self.getWeChatToken()
        url = self.downLoadVoiceUrl % (token, mediaID)

        ret = requests.get(url)
        with open(saveFile, "wb") as fh:
            fh.write(ret.content)

        pass

    def uploadVoiceFile(self, voiceFile):
        token = self.getWeChatToken()
        url = self.uploadVoiceUrl % token

        files = {"file" : open(voiceFile, "rb")}

        retMsg = ""
        try:
            ret = requests.post(url, files=files)
            retMsg = ret.json()["media_id"]
            print(retMsg)
        except Exception as Ex:
            traceback.print_exc()
        finally:
            return retMsg


    def downloadImageAsFile(self, mediaID, saveFile):
        token = self.getWeChatToken()
        url = self.downLoadIMGUrl % (token, mediaID)

        ret = requests.get(url)
        with open(saveFile, "wb") as fh:
            fh.write(ret.content)


    def uploadImageFile(self, imgFile):
        token = self.getWeChatToken()
        url = self.uploadImageUrl % token

        files = {"file": open(imgFile, "rb")}

        retMsg = ""
        try:
            ret = requests.post(url, files=files)
            retMsg = ret.json()["media_id"]
            print(retMsg)
        except Exception as Ex:
            traceback.print_exc()
        finally:
            return retMsg


    #send MSG to dedicated group with ID
    def send2Group(self, groupID):
        pass

    def send2All(self):
        pass