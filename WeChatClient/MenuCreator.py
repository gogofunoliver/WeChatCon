import requests
import json
from WechatHandler import WeChatHandler

class MenuCreator(object):
    def __init__(self):
        self.token_flag = "@@ACCESS_TOKEN@@"
        self.urlAPI = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
        self.custMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token=%s"


        self.jason_template = {
            "button" : [
                {
                    "type": "view",
                    "name": "Register",
                    "url": "http://facerecongwebapp-env.ap-northeast-1.elasticbeanstalk.com/"
                }
            ]
          }

    def create_menu(self, token):
        #1 basic menu
        wechat_api = self.custMenuUrl % token
        str_json = json.dumps(self.custZHMenu, ensure_ascii=False)
        response = requests.post(wechat_api, data=str_json.encode("utf-8"))
        print(response.content)
        #response = requests.post(wechat_api, data=json.dumps(self.custENMenu).encode("utf-8"))
        #print(response.content)
        #response = requests.post(wechat_api, data=json.dumps(self.custAWSMenu).encode("utf-8"))
        #print(response.content)

if __name__ == '__main__':
    wh = WeChatHandler()
    menu_creator = MenuCreator()
    menu_creator.create_menu(wh.getWeChatToken())
