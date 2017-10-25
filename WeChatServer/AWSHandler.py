import requests
import json
import boto3
import traceback
import web
from WeChatCon import *
from DBHandler import DBHandler
import subprocess



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

        reply_msg = "ß"
        if response['dialogState'] == 'ReadyForFulfillment' and response['intentName'] == 'IdentifyUser':
            print(response['slots'])
            if response['slots']['​StaffID'] == '44006524':
                reply_msg = "OH! Oliver, it's you. You are my father. What can I do for you?"
        else:
            reply_msg = response['message']
        print(reply_msg)
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

            if response['dialogState'] == 'ReadyForFulfillment' and response['intentName'] == 'IdentifyUser':
                #print(response['slots'])
                if response['slots']['StaffID'] == str('624'):
                    reply_msg = "OH! Oliver, it's you. You are my father. What can I do for you?"
                else:
                    reply_msg = "What can I do for you?"
                #call Polly
                VoiceGenerator().genVoiceByPolly(reply_msg, saveFile)
                reply_type = 'mp3'
            else:
                reply_msg = response['message']
                reply_type = "wav"
                print(response['inputTranscript'])
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


if __name__ == "__main__":
    VoiceGenerator().genVoiceByPolly("You are my boss. I am very happy to serve you!")
