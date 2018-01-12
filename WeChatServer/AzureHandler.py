# -*- coding: utf-8 -*-
# filename: AzureHandler.py

import requests
import json
import os
import traceback
from time import sleep


class AzureHandler(object):
    def __init__(self):
        self.key = os.environ.get('AZURE_KEY', 'Unknown')
        pass

    def create_profile(self):
        url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        data = {
                "locale": "zh-CN"
        }
        ret = requests.post(url, headers=headers, data=json.dumps(data))
        print("%d : %s" % (ret.status_code, ret.content))
        pass


    def get_op_status(self, op_location):
        #url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/operations/9fbbfd6f-a9fb-4e8f-be1d-12d9817dbbd9"
        url = op_location
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }
        ret = requests.get(url, headers=headers)
        json_ret = ret.json()
        print("%d : %s" % (ret.status_code, json.dumps(json_ret, indent=4, sort_keys=False, ensure_ascii=False)))
        return json_ret


    def index_voice_person(self, profile = "9f342db7-4f24-492c-bdd1-aadea49ac503", voice_file = "/tmp/voice.wav" ):
        op_result = {}
        try:
            url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles/%s/enroll" % profile

            #voice_file = "/Users/olivershen/Desktop/oliver.wav"
            with open(voice_file, "rb") as voice_f:
                data = voice_f.read()

            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': self.key,
            }
            ret = requests.post(url, data=data, headers=headers)
            op_location = ret.headers['Operation-Location']
            print("%d : %s" % (ret.status_code, op_location))

            op_result = self.get_op_status(op_location)
            '''
            while (op_result['status'] == "running"):
                sleep(1)
                op_result = self.get_op_status(op_location)
            '''
        except Exception as ex:
            traceback.print_exc()
        finally:
            print(op_result)


    def verify_user(self, profile = "9f342db7-4f24-492c-bdd1-aadea49ac503", voice_file = "/tmp/oliver.wav"):
        url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/verify?verificationProfileId=%s" % profile
        voice_file = "/Users/olivershen/Desktop/oliver2.wav"
        with open(voice_file, "rb") as voice_f:
            data = voice_f.read()

        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': self.key,
        }
        ret = requests.post(url, data=data, headers=headers)
        json_ret = ret.json()
        print("%d : %s" % (ret.status_code, json.dumps(json_ret, indent=4, sort_keys=False, ensure_ascii=False)))


    def identify_user(self, profile_id, voice_file):
        try:
            url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identify"
            #profiles = ",".join(profile_id)
            #print(profiles)
            parameters = {
                "identificationProfileIds": profile_id,
                "shortAudio" : "true",
            }

            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Ocp-Apim-Subscription-Key': self.key,
            }
            print(voice_file)
            #voice_file = "/Users/olivershen/Desktop/Sample_Voice/oliver2.wav"
            with open(voice_file, "rb") as voice_f:
                data = voice_f.read()

            ret = requests.post(url, data=data, params=parameters, headers=headers)
            op_location = ret.headers['Operation-Location']
            print("%d : %s" % (ret.status_code, op_location))

            op_result = self.get_op_status(op_location)
            while (op_result['status'] != "succeeded" and
                           op_result['status'] != "failed"):
                sleep(1)
                op_result = self.get_op_status(op_location)
        except Exception as ex:
            traceback.print_exc()
        finally:
            result = False
            if op_result['status'] == "succeeded" and \
                op_result['processingResult']['identifiedProfileId'] == profile_id:
                result = True
            return result


    def get_all_profile(self):
        url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }
        ret = requests.get(url, headers=headers)
        json_ret = ret.json()
        print("%d : %s" % (ret.status_code, json.dumps(json_ret, indent=4, sort_keys=False, ensure_ascii=False)))


    def get_profile(self, profile_id = "de62bb89-20c4-449a-a70f-b2ef8bcaeba3"):
        url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles/" + profile_id

        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        ret = requests.get(url, headers=headers)
        json_ret = ret.json()
        print("%d : %s" % (ret.status_code, json.dumps(json_ret, indent=4, sort_keys=False, ensure_ascii=False)))


if __name__ == "__main__":
    #AzureHandler().index_voice_person("34aed66e-509d-4ed3-9355-630733bed1cb", "/Users/olivershen/Desktop/Sample_Voice/lulu.wav")
    AzureHandler().get_all_profile()
    #AzureHandler().get_profile()
    #AzureHandler().verify_user("248cf092-55c1-4403-a3a2-c27565a56e22", )
    AzureHandler().identify_user("de62bb89-20c4-449a-a70f-b2ef8bcaeba3", voice_file="/tmp/gogofun/voice_oHBF6wUHaE4L2yUfhKMBqcrjoi0g_20180109092309.wav")
