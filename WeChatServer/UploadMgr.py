# -*- coding: utf-8 -*-
# filename: main.py
import web
import traceback
import json


class UploadMgr(object):
    def GET(self):
        output = ""
        try:
            data = web.input()
            if len(data) == 0:
                output = "hello, this is UploadMgr view"
            else:
                output = "Test"

        except Exception as Argument:
            traceback.print_exc()
        finally:
            return output

    def POST(self):
        output = ""
        try:
            webData = web.data().decode('utf-8')
            aws_msg = json.loads(webData)

            output = aws_msg["message"]

        except Exception as Argment:
            traceback.print_exc()
            return output


