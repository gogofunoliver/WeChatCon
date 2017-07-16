import requests
import json
import traceback
import web
from WeChatCon import *

class AWSHandler(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            return "Test"

        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data().decode('utf-8')
            message_to_send = json.loads(webData)["message"]
            wechat_con = WeChatHandler()
            if int(wechat_con.sendMsgToOneAsPreview(message_to_send, "touser", "oHBF6wUHaE4L2yUfhKMBqcrjoi0g")) == 0:
                return "sending to wechat successfully"
            else:
                return "failed sending to wechat"

        except Exception as Argment:
            traceback.print_exc()
            return Argment