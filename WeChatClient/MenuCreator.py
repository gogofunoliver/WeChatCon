import requests
import json
from WechatHandler import WeChatHandler

class MenuCreator(object):
    def __init__(self):
        self.token_flag = "@@ACCESS_TOKEN@@"
        self.urlAPI = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
        self.custMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token=%s"

        self.custAWSMenu = \
            {
                "button": [
                    {
                        "type": "click",
                        "name": "History Alert",
                        "key": "HistoryAlert"
                    },
                    {
                        "name": "EC2 ",
                        "sub_button":
                            [
                                {
                                    "type": "click",
                                    "name": "Apply EC2",
                                    "key": "ApplyVM"
                                },
                                {
                                    "type": "click",
                                    "name": "Del EC2",
                                    "key": "RemoveVM"
                                }
                            ]
                    },
                    {
                        "type": "click",
                        "name": "About Me",
                        "key": "About_Me"
                    }
                ],
                "matchrule":
                    {
                        "tag_id": "104"
                    }
            }

        self.jason_template = {
            "button" : [
                {
                    "type": "click",
                    "name": "设置中文",
                    "key": "SetZH"
                },
                {
                    "type": "click",
                    "name": "Set English",
                    "key": "SetEN"
                },
                {
                    "type": "click",
                    "name": "Set Cantonese",
                    "key": "SetCT"
                },
            ]
        }
        self.custENMenu = \
            {
                "button":[
                            {
                                "type":"click",
                                "name":"History",
                                "key":"History"
                            },
                            {
                                "name":"ChinaGo",
                                "sub_button":
                                [
                                    {
                                        "type":"click",
                                        "name":"Foody",
                                        "key":"Foody"
                                    },
                                    {
                                        "type":"click",
                                        "name":"Tourist",
                                        "key":"Tourist"
                                    }
                                ]
                            },
                            {
                                "type": "click",
                                "name": "Joke",
                                "key": "MA_JOKE"
                            }
                          ],
                "matchrule":
                {
                      "language":"en"
                 }
            }

        self.custZHMenu = {
                "button":[
                            {
                                "type":"click",
                                "name":"历史文章",
                                "key":"History",
                            },
                            {
                                "name":"天下",
                                "sub_button":
                                [
                                    {
                                        "type":"click",
                                        "name":"吃天下",
                                        "key":"Foody",
                                    },
                                    {
                                        "type":"click",
                                        "name":"看天下",
                                        "key":"Tourist",
                                    }
                                ]
                            },
                            {
                                "type": "click",
                                "name": "马儿爱段子",
                                "key": "Joke",
                            }
                          ],
                "matchrule":
                {
                      "language":"zh_CN"
                 },
            }

    def create_menu(self, token):
        #1 basic menu
        wechat_api = self.urlAPI % token
        delete_api = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % token
        ret = requests.get(delete_api)
        print(ret.content)
        response = requests.post(wechat_api, data=json.dumps(self.jason_template, ensure_ascii=False).encode("utf-8"))
        print(response.content)
        '''
        wechat_api = self.custMenuUrl % token
        str_json = json.dumps(self.custZHMenu, ensure_ascii=False)
        response = requests.post(wechat_api, data=str_json.encode("utf-8"))
        print(response.content)
        response = requests.post(wechat_api, data=json.dumps(self.custENMenu).encode("utf-8"))
        print(response.content)
        response = requests.post(wechat_api, data=json.dumps(self.custAWSMenu).encode("utf-8"))
        print(response.content)
       '''
if __name__ == '__main__':
    wh = WeChatHandler()
    menu_creator = MenuCreator()
    menu_creator.create_menu(wh.getWeChatToken())
