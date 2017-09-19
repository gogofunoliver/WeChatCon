import requests
import traceback
import json
import os
import base64
import sys
from WeChatCon import WeChatHandler
from TypeDef import TypeDef


class GoogleCaller(object):
    def __init__(self):
        pass

    def callGoogle(self, mediaID, users):
        try:
            url_base = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"
            token = WeChatHandler().getWeChatToken()
            url = url_base % (token, mediaID)

            ret = requests.get(url)
            #py can not get the size of c type variable
            #audo_size = sys.getsizeof(ret.content)
            audio_str = base64.b64encode(ret.content)

            #store the last voice as tmp file
            with open("/tmp/voice_test.amr", "wb") as temp_voice:
                temp_voice.write(ret.content)

            #baidu, parse bytes audio
            output_baidu = BaiduCaller().callBaidu(audio_str)
            reply_msg = "百度识别：" + output_baidu
            WeChatHandler().sendMsgViaCust(reply_msg, "touser", users)
            #ali

            #google
            google_rec = "http://google2:18080/google"
            msg = {
                "audio" : str(audio_str, encoding="utf-8"),
                "lang" : TypeDef.LANG,
            }

            ret = requests.post(google_rec, data=json.dumps(msg))
            outcome = json.loads(ret.content.decode("utf-8"))
            reply_msg = "Google识别：%s\n语气：%s\n语气强度：%s" %  \
                        (outcome['Google识别'][0]['transcript'], outcome['语气'], outcome['语气强度'])
            #WeChatHandler().sendMsgToOneAsPreview(outcome)
            WeChatHandler().sendMsgViaCust(reply_msg, "touser", users)
            #WeChatHandler().sendMsgToOneAsPreview(outcome, "touser", users)
        except Exception as ex:
            traceback.print_exc()
            raise ex


class BaiduCaller(object):
    def __init__(self):
        self.api_key = os.environ.get("BAIDU_API_KEY", None).strip()
        self.sec_key = os.environ.get("BAIDU_SEC_KEY", None).strip()
        self.baiduVoiceUrl = "http://vop.baidu.com/server_api"
        get_token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (self.api_key, self.sec_key)
        ret = requests.get(get_token_url)
        if ret.status_code == 200:
            self.token = ret.json()['access_token']
            #print("BaiduCaller init successfully, token = %s" % self.token)
        self.emotionAnalysis = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=%s" % self.token
        pass

    #audio, is bytes from wechat
    def callBaidu(self, base64byte, vocie_file="/tmp/voice_test.amr"):
        output = ""
        try:
            size_voice = os.path.getsize(vocie_file)
            str_speech = str(base64byte, encoding="gbk")
            if TypeDef.LANG == TypeDef.Event_SetEN:
                lang = "en"
            elif TypeDef.LANG == TypeDef.Event_SetZH:
                lang = "zh"
            elif TypeDef.LANG == TypeDef.Event_SetCT:
                lang = "ct"
            else:
                lang = "zh"

            baidu_input = {
                "format": "amr",
                "rate": 8000,
                "channel": 1,
                "token": self.token,
                "cuid": "test_from_oliver_wechat",
                "lan" : lang,
                "len": size_voice,
                "speech": str_speech,
            }
            ret = requests.post(self.baiduVoiceUrl, data=json.dumps(baidu_input))
            output = ret.json()['result'][0]
            output = output + "\n情感分析：\n" + self.analysisEmotion(output)
            pass
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            return output

    def analysisEmotion(self, text):
        message = ""
        try:
            baidu_input = {
                "text": text
            }
            ret = requests.post(self.emotionAnalysis, data=json.dumps(baidu_input).encode("gbk"))
            if ret.status_code == 200:
                message = "Positive可能，%s；Negative可能，%s" % (ret.json()['items'][0]['positive_prob'], ret.json()['items'][0]['negative_prob'])

        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            return message