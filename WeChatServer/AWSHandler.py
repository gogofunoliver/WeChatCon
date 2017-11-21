# -*- coding: utf-8 -*-
# filename: AWSHandler.py

import requests
import json
import boto3
import traceback
import web
from WeChatCon import *
from DBHandler import DBHandler
import subprocess
import time
from TypeDef import TypeDef
from GoogleNLP import *

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
            aws_msg = json.loads(webData)

            DBHandler().insert("INSERT into AWS_Record VALUES (null, '%s', '%s', '%s', '%s', null)"
                % (aws_msg['Region'], aws_msg['ResID'], aws_msg['message'], aws_msg['Resource']) )

            message_to_send = aws_msg["message"]
            wechat_con = WeChatHandler()
            if int(wechat_con.sendMsgToOneAsPreview(message_to_send, "touser", "oHBF6wRiecgOOlymR73g-Xa8OcD8")) == 0:
                return "sending to wechat successfully"
            else:
                return "failed sending to wechat"

        except Exception as Argment:
            traceback.print_exc()
            return Argment



class LexConnector(object):
    def __init__(self):
        self.lex_router = "http://google2:18080/lexcon"
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

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        reply_msg = ""
        if response['dialogState'] == 'ReadyForFulfillment':
            if response['intentName'] == 'IdentifyUser':
                print(response['slots'])
                if response['slots']['StaffID'] == '44006524':
                    reply_msg = "OH! Oliver, it's you. You are my father. What can I do for you?"
                    mediaID = WeChatHandler().uploadImageFile("/tmp/Oliver.jpg")
                    WeChatHandler().sendImageMsgCust(mediaID, userId)
                elif response['slots']['StaffID'] == "35022399":
                    reply_msg = "OH! Really?! You are Raymond O' Brien. My Father's Boss! What can I do for you?"
                    mediaID = WeChatHandler().uploadImageFile("/tmp/RayO.jpg")
                    WeChatHandler().sendImageMsgCust(mediaID, userId)
                elif response['slots']['StaffID'] == "20395370":
                    reply_msg = "OH! Really?! You are Gary Lee. My Father's Boss! What can I do for you?"
                    mediaID = WeChatHandler().uploadImageFile("/tmp/gary.jpg")
                    WeChatHandler().sendImageMsgCust(mediaID, userId)
                elif response['slots']['StaffID'] == "04756169":
                    reply_msg = "OH! Really?! You are Lee Ashmore, Our GCB 3 manager! What can I do for you?"
                    mediaID = WeChatHandler().uploadImageFile("/tmp/lee.jpg")
                    WeChatHandler().sendImageMsgCust(mediaID, userId)
                else:
                    reply_msg = "What can I do for you?"
            elif response['intentName'] == 'OpenAccount':
                reply_msg = "I have record your information and will inform you after it get approved. See you!"
                user_dict = WeChatHandler().getUserInfo(userId)
                tempSaveData = {
                    "OpenID": {"S": userId},
                    "WeChatName": {"S": user_dict['nickname']},
                    "Sex": {"S": TypeDef.sex_dict[user_dict['sex']]},
                    "Salary": {"S": response['slots']['Salary']},
                    "Company": {"S": response['slots']['Company']}, #
                    "JobPosition": {"S": response['slots']['JobPosition']},
                    "ApplyCardType": {"S": response['slots']['CreditCardType']},
                    "Province": {"S": user_dict['province']},
                    "Country": {"S": user_dict['country']},
                    "LastUpdate": {"S": timestamp}
                }
                DynamoDBWriter().put_item("UserInfoWeChat", tempSaveData)
                dataSort = {"ApplyCardType": response['slots']['CreditCardType'],
                            "Country": user_dict['country'],
                            "JobPosition": response['slots']['JobPosition'],
                            "Salary": response['slots']['Salary'],
                            "Sex": TypeDef.sex_dict[user_dict['sex']]}
                ret = AWSMLConnector().connect(dataSort)
                if ret == "1":
                    reply_msg = "Since you own the high credit in our bank,  we " \
                                "have a product you may be interested. Do you want to know more?"
                else:
                    reply_msg = "Thanks for you apply."
        else:
            reply_msg = response['message']
            process = GoogleNLPPorocesor()
            analysis = process.anlysisText(msg)
            Emotion = {
                "OpenID_Time": {"S" : userId + timestamp},
                "Magnitude" : {"S" : str(analysis["documentSentiment"]["magnitude"])},
                "OpenID" : {"S" : userId},
                "Sentiment" : {"S" : str(analysis["documentSentiment"]["score"])},
                "TimeStamp" : {"S" : timestamp},
                "Text" : {"S" : msg}
            }
            if analysis["documentSentiment"]["score"] < 0:
                #re write
                reply_msg = response['message'] + " (It seems you are unhappy. I will improve my ability to server you.)"
            DynamoDBWriter().put_item("UserEmotion", Emotion)
        print("******* %s" % reply_msg)
        WeChatHandler().sendMsgViaCust(reply_msg, to_user=userId)
        return reply_msg

    def connectVoice(self, userId = 'test_wechat_bot', msg = 'book hotel', saveFile = "/tmp/aws_rsp.wav"):
        reply_type = "wav"
        reply_msg = ""
        try:
            client = boto3.client('lex-runtime')
            response = client.post_content(
                botName = 'BookTrip',
                botAlias = 'dev',
                userId = userId,
                contentType = 'audio/lpcm; sample-rate=8000; sample-size-bits=16; channel-count=1; is-big-endian=false',
                accept = 'audio/mpeg',
                inputStream = msg
            )

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if response['dialogState'] == 'ReadyForFulfillment':
                if response['intentName'] == 'IdentifyUser':
                    #print(response['slots'])
                    if response['slots']['StaffID'] == str('624'):
                        reply_msg = "OH! Oliver, it's you. You are my father. What can I do for you?"
                        mediaID = WeChatHandler().uploadImageFile("/tmp/Oliver.jpg")
                        WeChatHandler().sendImageMsgCust(mediaID, userId)
                    elif response['slots']['StaffID'] == str('399'):
                        reply_msg = "OH! Really?! You are Ray O' Brien. My Father's Boss! I can give you some discount. " \
                                    "Please don't tell to other people. Anyway, What can I do for you now?"
                        #VoiceGenerator().genVoiceByPolly(reply_msg, saveFile)
                        #mediaID = WeChatHandler().uploadVoiceFile(saveFile)
                        #WeChatHandler().sendVoiceMsgCust(mediaID, userId)
                        mediaID = WeChatHandler().uploadImageFile("/tmp/RayO.jpg")
                        WeChatHandler().sendImageMsgCust(mediaID, userId)
                    elif response['slots']['StaffID'] == str('370'):
                        reply_msg = "OH! Really?! You are Gary Lee. My Father's Boss! I can give you some discount. " \
                                    "Please don't tell to other people. Anyway, What can I do for you now?"
                        #VoiceGenerator().genVoiceByPolly(reply_msg, saveFile)
                        #mediaID = WeChatHandler().uploadVoiceFile(saveFile)
                        #WeChatHandler().sendVoiceMsgCust(mediaID, userId)
                        mediaID = WeChatHandler().uploadImageFile("/tmp/gary.jpg")
                        WeChatHandler().sendImageMsgCust(mediaID, userId)
                    elif response['slots']['StaffID'] == "169":
                        reply_msg = "OH! Really?! You are Lee Ashmore, Our GCB 3 manager! What can I do for you?"
                        mediaID = WeChatHandler().uploadImageFile("/tmp/lee.jpg")
                        WeChatHandler().sendImageMsgCust(mediaID, userId)
                    else:
                        reply_msg = "What can I do for you?"
                elif response['intentName'] == 'OpenAccount':
                    reply_msg = "I have record your information and will inform you after it get approved. See you!"
                    user_dict = WeChatHandler().getUserInfo(userId)
                    tempSaveData = {
                        "OpenID" : {"S" : userId},
                        "WeChatName" : {"S" : user_dict['nickname']},
                        "Sex" : {"S" : TypeDef.sex_dict[user_dict['sex']]},
                        "Salary" : {"S" : response['slots']['Salary']},
                        "Company" : {"S": response['slots']['Company']},
                        "JobPosition" : { "S" : response['slots']['JobPosition']},
                        "ApplyCardType" : {"S" : response['slots']['CreditCardType']},
                        "Province" : {"S" : user_dict['province']},
                        "Country" : {"S" : user_dict['country']},
                        "LastUpdate" : {"S" : timestamp}
                        }
                    DynamoDBWriter().put_item("UserInfoWeChat", tempSaveData)
                    dataSort = {"ApplyCardType" : response['slots']['CreditCardType'],
                        "Country" : user_dict['country'],
                        "JobPosition" : response['slots']['JobPosition'],
                        "Salary" : response['slots']['Salary'],
                        "Sex" : TypeDef.sex_dict[user_dict['sex']]}
                    ret = AWSMLConnector().connect(dataSort)
                    if ret == "1":
                        reply_msg = "Since you own the high credit in our bank,  we" \
                                    "have a product you may be interested. Do you want to know more?"
                    else:
                        reply_msg = "That's all done. Thanks for your apply."
                # call Polly
                VoiceGenerator().genVoiceByPolly(reply_msg)
                reply_type = 'mp3'
                pass
            else:
                reply_type = "wav"
                print(response['inputTranscript'])

                #call GCP
                process = GoogleNLPPorocesor()
                analysis = process.anlysisText(response['inputTranscript'])
                Emotion = {
                    "OpenID_Time": {"S": userId + timestamp},
                    "Magnitude": {"S": str(analysis["documentSentiment"]["magnitude"])},
                    "OpenID": {"S": userId},
                    "Sentiment": {"S": str(analysis["documentSentiment"]["score"])},
                    "TimeStamp": {"S": timestamp},
                    "Text": {"S": response['inputTranscript']}
                }
                print(analysis["documentSentiment"]["score"])
                if analysis["documentSentiment"]["score"] < 0:
                    # re write
                    reply_msg = "It seems you are unhappy. Please take care and " + response['message']
                    VoiceGenerator().genVoiceByPolly(reply_msg)
                    reply_type = "mp3"

                DynamoDBWriter().put_item("UserEmotion", Emotion)

                #save voice file from Lex
                rsp = response['audioStream']
                data = rsp.read()
                with open(saveFile, "wb") as aws_rsp:
                    aws_rsp.write(data)
        except Exception as ex:
            traceback.print_exc()
        finally:
            print(reply_msg)
            return reply_type

class VoiceGenerator(object):
    def __init__(self):
        self.client = boto3.client('polly')
        pass

    def genVoiceByPolly(self, text, saveFile = "/tmp/polly.mp3", performer = "Salli"):
        response = self.client.synthesize_speech(
            OutputFormat = 'mp3', #mp3, pcm can be supported
            SampleRate = '16000',
            Text = text,
            TextType = 'text',
            VoiceId = performer
        )

        rsp = response['AudioStream']
        data = rsp.read()
        with open(saveFile, "wb") as aws_rsp:
            aws_rsp.write(data)

class DynamoDBWriter(object):
    def __init__(self):
        self.client = boto3.client('dynamodb')
        pass

    def put_item(self, table, item_dict=None):
        response = ""
        try:
            response = self.client.put_item(TableName=table, Item=item_dict)
        except Exception as ex:
            traceback.print_exc()
        finally:
            return response


class AWSMLConnector(object):
    def __init__(self):
        self.client = boto3.client('machinelearning')
        pass

    def connect(self, items):
        response = self.client.predict(
            MLModelId='ml-GEScpmbcQ5b',  #"ml-buX245aEYd6",
            Record={"ApplyCardType" : items['ApplyCardType'],
                    "Country" : items['Country'],
                    "JobPosition" : items['JobPosition'],
                    "Salary" : items['Salary'],
                    "Sex" : items['Sex']
                    },
            PredictEndpoint="https://realtime.machinelearning.us-east-1.amazonaws.com"
        )
        print(response['Prediction'])
        return response['Prediction']['predictedLabel']
        pass
        '''
        {
            "Prediction": {
            "Prediction": {
            
            
                "details": {
                    "Algorithm": "SGD",
                    "PredictiveModelType": "BINARY"
                },
                "predictedLabel": "0",
                "predictedScores": {
                    "0": 0.00021320235100574791
                }
        }
        '''



if __name__ == "__main__":
    data = {
        "ApplyCardType" : "Normal" ,
        "Country" : "China",
        "JobPosition" : "CEO",
        "Salary": "99999",
        "Sex" : "mail"
    }
    AWSMLConnector().connect(data)
