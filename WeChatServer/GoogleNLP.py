# -*- coding: utf-8 -*-
# filename: GoogleNLP.py
# oliver

import traceback
import requests
import json
import os
import web
import base64

class GoogleNLPPorocesor(object):
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_KEY', 'Unknown')
        pass


    def voiceToText(self, voiceInput, lang = "en-US"):
        content = ""
        try:
            if lang == "SetZH":
                language = "cmn-Hans-CN"
            elif lang == "SetEN":
                language = "en-US"
            elif lang == "SetCT":
                language = "yue-Hant-HK"
            else:
                language = "en-US"

            google_nlp_input = {
                "config":
                    {
                        "encoding": "AMR",
                        "sampleRateHertz": 8000,
                        "languageCode": language,
                        "enableWordTimeOffsets": False
                    },
                "audio":
                    {
                        "content": voiceInput
                    }
            }

            google_rec = "https://speech.googleapis.com/v1/speech:recognize?key=%s" % self.api_key
            ret = requests.post(google_rec, data=json.dumps(google_nlp_input).encode('utf-8'))
            alternatives = ret.json()['results'][0]['alternatives']

            #reply_msg = ""
            #for text in alternatives:
                #line_msg = "Google recognition: %s. Confidence: %s" % (text['transcript'], text['confidence'])
                #content = content + text['transcript']
                #reply_msg = line_msg + "\n" + reply_msg

        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            return alternatives

    def entityAnalysis(self, content):
        content_reply = ""
        try:
            google_anysis = "https://language.googleapis.com/v1beta2/documents:analyzeEntities?key=%s" % self.api_key
            anysis = {
                "document":
                {
                    "type": "PLAIN_TEXT",
                    "content": content
                },
                "encodingType": "UTF8"
            }

            ret = requests.post(google_anysis, data=json.dumps(anysis).encode('utf-8'))
            content_reply = json.dumps(ret.json())

        except Exception as ex:
            traceback.print_exc()
        finally:
            return content_reply

    def sentimentAnalysis(self,content):
        content_reply = ""
        try:
            anysis = {
                "document":
                    {
                        "type": "PLAIN_TEXT",
                        "content": content
                    },
                "encodingType": "UTF8"
            }

            googleSentiment = "https://language.googleapis.com/v1beta2/documents:analyzeSentiment?key=%s" % self.api_key
            ret = requests.post(googleSentiment, data=json.dumps(anysis).encode('utf-8'))
            content_reply = "magnitude: %d, score: %d" % (ret.json()['documentSentiment']['magnitude'],
                ret.json()['documentSentiment']['score'])
            #content_reply = json.dumps(ret.json())
        except Exception as ex:
            traceback.print_exc()
        finally:
            return content_reply

    def anlysisText(self, content):
        reply_cont = ""
        try:
            google_input = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": content
                },
                "features": {
                    "extractEntities": True,
                    "extractDocumentSentiment": True,
                },
                "encodingType": "UTF8",
            }

            google_txt = "https://language.googleapis.com/v1beta2/documents:annotateText?key=%s" % self.api_key
            ret = requests.post(google_txt, data=json.dumps(google_input))
            ret.encoding = 'utf-8'
            reply_cont = ret.json()

        except Exception as ex:
            traceback.print_exc()
        finally:
            return reply_cont


    def getTextFromImage(self, imageContent):
        analysis_url = "https://vision.googleapis.com/v1/images:annotate?key=%s" % self.api_key

        request_data = {
            "requests" : [
                {
                    "image" : {
                        "content" : imageContent
                    },
                    "features" : [
                        {
                            "type" : "TEXT_DETECTION"
                        }
                    ]

                }
            ]
        }
        ret = requests.post(analysis_url, data=json.dumps(request_data))
        result = ret.json()
        return result
        pass


    def photoAnalysis(self):
        pass



if __name__ == "__main__":
    content = ""
    with open("/tmp/aobama.jpg", "rb") as reader:
        content = reader.read()
    str_content = str(base64.b64encode(content), encoding="utf-8")
    result = GoogleNLPPorocesor().getTextFromImage(str_content)
    print(result['responses'][0]['fullTextAnnotation']['text'])
    '''
        for sub_json in result['responses'][0]['textAnnotations']:
            print(sub_json['description'])
    '''




