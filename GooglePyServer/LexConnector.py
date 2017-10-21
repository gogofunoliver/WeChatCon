import requests
import json
import boto3
import web
import traceback

class LexConnector(object):
    def __init__(self):
        pass

    def connect(self, userId = 'test_wechat_bot', msg = 'book hotel'):
        client = boto3.client('lex-runtime')
        response = client.post_content(
            botName = 'BookTrip',
            botAlias = 'dev',
            userId = userId,
            contentType = 'text/plain; charset=utf-8',
            accept = 'text/plain; charset=utf-8',
            inputStream = msg.encode('utf-8')
        )
        print(response['message'])
        return response['message']

    def GET(self):
        content = ""
        try:
            data = web.input()
            if len(data) == 0:
                content = "hello, this is LexConnector view"
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
        return_str = ""
        try:
            webData = web.data()
            all_input = json.loads(webData.decode())
            #Jason Sample
            # {
            #    "OpenID" : "********"
            #    "message" : "******"
            # }

            openID = all_input['OpenID']
            msg_wechat = all_input['message']

            return_str = self.connect(openID, msg_wechat)

        except Exception as ex:
            traceback.print_exc()
        finally:
            return return_str


if __name__ == '__main__':
    LexConnector().connect()
    pass
