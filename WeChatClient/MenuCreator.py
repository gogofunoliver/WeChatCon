import requests
import json
from WechatHandler import WeChatHandler

class MenuCreator(object):
    def __init__(self):
        self.token_flag = "@@ACCESS_TOKEN@@"
        self.urlAPI = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=@@ACCESS_TOKEN@@"
        self.jason_template =  '{ \
         "button":[  \
            {	       \
               "name":"资源监视",  \
                  "sub_button" : [ \
                     { \
                        "type":"view", \
                        "name":"AWS资源",   \
                        "url":"https://us-east-1.signin.aws.amazon.com/oauth?SignatureVersion=4&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJMOATPLHVSJ563XQ&X-Amz-Date=2017-04-13T07%3A25%3A55.834Z&X-Amz-Signature=582ef25b56d52b4593168715fb8c371f19ba8fd06103164817d7e6112c4e9dd0&X-Amz-SignedHeaders=host&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fhomepage&redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue&response_type=code&state=hashArgs%23"  \
                     }, \
                     { \
                        "type":"click", \
                        "name":"Ambari资源",   \
                        "key":"AMBARI_CHECK"  \
                     }, \
                     { \
                        "type":"view", \
                        "name":"公积金查询",   \
                        "url":"http://query.xazfgjj.gov.cn/"  \
                     } \
                  ] \
            },  \
            {   \
               "name":"天下",  \
               "sub_button":[  \
                    {	\
                       "type":"click", \
                       "name":"吃世界",   \
                       "key":"FOODY"  \
                    }, \
                    {	\
                        "type":"click", \
                        "name":"看世界",   \
                        "key":"TRAVEL"  \
                    } \
                ]  \
            }, \
            {   \
                "name":"怼人机器",  \
                 "sub_button":[  \
                     {	\
                        "type":"click", \
                        "name":"马儿爱吃草",   \
                        "key":"MA_CHI"  \
                      }, \
                      {	\
                         "type":"click", \
                         "name":"马儿爱睡觉",   \
                         "key":"MA_SLEEP"  \
                       } \
                  ]  \
             } \
        ]  \
        }'


    def create_menu(self, token):
        wechat_api = self.urlAPI.replace(self.token_flag, token)
        response = requests.post(wechat_api, data=self.jason_template.encode("utf-8"))
        print(response.content)

if __name__ == '__main__':
    wh = WeChatHandler()
    menu_creator = MenuCreator()
    menu_creator.create_menu(wh.getWeChatToken())
