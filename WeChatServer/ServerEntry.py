# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import traceback
import receive
import reply
from UserHandler import UserHandler
from FileHandler import FileHandler
import traceback
import logging
from Operator import *
from Resource import *
from HealthyNotifier import HealthyNotifier
from ActionHandler import ActionsExecutor
from WeChatEventHandler import EventRouter
from TypeDef import TypeDef
from WeChatDownload import GoogleCaller
from AWSHandler import  *
from VoiceFormater import VoiceFormater

class Handle(object):
    def __init__(self):
        self.logger = logging.getLogger("root.ServerEntry")

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            #wechat authoticaiton
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "hellogoogle"

            print("token: %s" % token)
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            #print "handle/GET func: hashcode {0}, signature : {1} ".format(hashcode, signature))
            print("handle/GET func: hashcode: {0}, signature: {1}".format(hashcode, signature))
            if hashcode == signature:
                #return echostr
            #else:
                return ""
            return echostr

        except Exception as Argument:
            traceback.print_exc()
            return Argument

    def POST(self):
        try:
            webData = web.data()
            self.logger.info("Handle Post webdata is {0}".format(webData))
            recMsg = receive.parse_xml(webData)
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = ""

            user_info = WeChatHandler().getUserInfo(toUser)
            if user_info['subscribe'] == 0:
                lang = "en"
            else:
                lang = user_info['language']

            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'voice':
                if recMsg.Recognition is None or len(recMsg.Recognition) == 0:
                    content = "Invalid Message"
                else:
                    user_say = recMsg.Recognition#.replace("。", "").replace("，", "")
                    content = Resource.getMsg("USay") + user_say + "\n" + "Media ID: " + recMsg.MediaId + "\n"
                    #content = self.callAWSLex(toUser, fromUser, recMsg.MediaId)

                    #content = "微信识别：" + user_say
                    #ActionsExecutor.add_auto_action(Action(GoogleCaller().callGoogle, recMsg.MediaId, toUser))
                    ActionsExecutor.add_auto_action(Action(self.callAWSLex, toUser, fromUser, recMsg.MediaId))
                    return "success"
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                cnstr = recMsg.Content.decode()
                self.logger.info("received msg : %s" % cnstr)
                content = self.callAWSLexWithText(toUser, fromUser, cnstr)
                #ActionsExecutor.add_auto_action(Action(self.callAWSLexWithText, toUser, fromUser, cnstr))
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'event':
                    func = EventRouter.get_envent_func(recMsg.event, recMsg.key_value)
                    content = func(toUser)
            else:
                content = Resource.getMsg("WrongTypeMsg", lang)

            if content is None or len(content) == 0:
                return "success"
            else:
                self.logger.info("Reply : %s" % content)
                #print(content)
                return content

        except Exception as Argment:
            traceback.print_exc()
            return Argment


    def unitTest1(self):
        pass
        '''
                      if user_say == TypeDef.OP_Delete_VM:
                          action_str = user_say
                          msg_str = ""
                      elif user_say == TypeDef.OP_Create_VM:
                          action_str = user_say
                          msg_str = ""
                      #e.g. 记录测试测试测试测试。。。> 4
                      elif len(user_say) >= 4 and user_say[0:2] == TypeDef.OP_Write:
                          action_str = TypeDef.OP_Write
                          msg_str = user_say[2:]
                      #天气查询，天气订阅，取消订阅，历史记录
                      elif len(user_say) >= 4:
                          #non-record operaiton
                          action_str = user_say[0:4]
                          msg_str =  user_say[4:]
                      elif len(user_say) == 1:
                          action_str = user_say
                          msg_str = ""
                      else:
                          action_str = user_say[0:2]
                          msg_str = user_say[2:]

                      check_resoult = HealthyNotifier.get_instance().check_wait(toUser, user_say)
                      if check_resoult == "":
                          func = OperationType.get_operate_function(action_str)
                          if func == TypeDef.Undefined:
                              if ActionsExecutor.has_manual_actions(toUser):
                                  content += ActionsExecutor.exuecte_actions(toUser, action_str)
                              else:
                                  content += Resource.getMsg("Unidentified", lang) + "\n" + Resource.getMsg("Menu", lang)
                          else:
                              content += func(msg_str, recMsg.FromUserName, lang)
                      else:
                          content += check_resoult
        '''

    def unitTest2(self):
        pass
        '''
                      action_str = cnstr.split(" ", 1)[0]
                      if action_str == cnstr:
                          msg_str = ""
                      else:
                          msg_str = cnstr.split(" ", 1)[1].strip()

                      content = HealthyNotifier.get_instance().check_wait(toUser, cnstr)
                      if content == "":
                          func = OperationType.get_operate_function(action_str)
                          if func == TypeDef.Undefined:
                              if ActionsExecutor.has_manual_actions(toUser):
                                  content = ActionsExecutor.exuecte_actions(toUser, action_str)
                              else:
                                  content = Resource.getMsg("Unidentified", lang) + "\n" + Resource.getMsg("Menu", lang)
                          else:
                              content = func(msg_str, recMsg.FromUserName, lang)

        '''

    def callAWSLex(self, toUser, fromUser, mediaID, isAysnc = "Y"):
        content = ""
        try:
            # define temp file to save the voice
            saveWeChatAMRFile = "/tmp/wechat_tmp_voice.amr"
            saveWeChatWAVFile = "/tmp/wechat_tmp_voice.wav"
            saveAWSWAVFile = "/tmp/aws_reply_voice.wav"
            saveAWSAMRFile = "/tmp/aws_reply_voice.amr"

            # 1. Get WeChat Voice
            WeChatHandler().downloadVoiceAsFile(mediaID, saveWeChatAMRFile)

            # 2 change format to wavsaveWeChatWAVFile
            VoiceFormater().amr2wav(saveWeChatAMRFile, saveWeChatWAVFile)

            with open(saveWeChatWAVFile, "rb") as fh:
                rspData = fh.read()

            # 3 Call Lex
            if LexConnector().connectVoice(toUser, rspData, saveAWSWAVFile) == 'mp3':
                mediaReplyID = WeChatHandler().uploadVoiceFile("/tmp/polly.mp3")
            else:
                VoiceFormater().wav2amr(saveAWSWAVFile, saveAWSAMRFile)
                mediaReplyID = WeChatHandler().uploadVoiceFile(saveAWSAMRFile)

            replier = reply.VoiceMsg(toUser, fromUser, mediaReplyID)
            content = replier.send()

            if isAysnc == "Y":
                WeChatHandler().sendVoiceMsgCust(mediaReplyID, toUser)
                content = "success"
        except Exception as ex:
            traceback.print_exc()
        finally:
            print(content)
            return content

    def callAWSLexWithText(self, toUser, fromUser, msg):
        content = LexConnector().connect(toUser, msg)
        replier = reply.TextMsg(toUser, fromUser, content)
        content = replier.send()
        return content
