# -*- coding: utf-8 -*-
# filename: GoogleHanlder.py
# oliver

import requests
import json
import traceback
import web

from GoogleNLP import GoogleNLPPorocesor

class GoogleHanlder(object):
    def GET(self):
        content = ""
        try:
            data = web.input()
            if len(data) == 0:
                content = "hello, this is handle view"
            else:
                content = "Test"
        except Exception as ex:
            content = ex.message
            raise ex
        finally:
            return content

    def POST(self):
        text = ""
        analysis = {}
        try:
            webData = web.data()
            all_input = json.loads(webData)
            audio = all_input['audio']
            lang = all_input['lang']
            process = GoogleNLPPorocesor()
            #google
            text = process.voiceToText(audio, lang)
            print(text)
            analysis = process.anlysisText(text[0]['transcript'])
            print(analysis)
            #baidu, ali, iflk
            #*****
        except Exception as ex:
            traceback.print_exc()
        finally:
            reply_msg = {
                u"Google识别" : text,
                u"语气" : analysis["documentSentiment"]["score"],
                u"语气强度" : analysis["documentSentiment"]["magnitude"],
                u"名词提取" : analysis["entities"],
            }
            return_str = json.dumps(reply_msg, ensure_ascii=False, indent=4)
            return return_str