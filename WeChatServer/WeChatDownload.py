import requests
import json
import os
import base64
from WeChatCon import WeChatHandler


class GoogleCaller(object):
    def __init__(self):
        pass

    def callGoogle(self, mediaID, users):
        try:
            url_base = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"
            token = WeChatHandler().getWeChatToken()
            #media = "CeQ8DBUS96TaubeeJnMjfBLXLE8JWJtnUduofsLMVWMaYI1OkHxxmNCy4oesyZPm"
            url = url_base % (token, mediaID)

            ret = requests.get(url)
            audio_str = base64.b64encode(ret.content)

            google_rec = "http://google2:18080/google"
            msg = str(audio_str, encoding='utf-8')
            #baidu

            #ali

            #google
            ret = requests.post(google_rec, data=msg)
            outcome = ret.content.decode("utf-8")
            #WeChatHandler().sendMsgToOneAsPreview(outcome)
            WeChatHandler().sendMsgViaCust(outcome, "touser", users)
            #WeChatHandler().sendMsgToOneAsPreview(outcome, "touser", users)
        except Exception as ex:
            print(ex)
            raise ex
