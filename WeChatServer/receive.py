# -*- coding: utf-8 -*-
# filename: receive.py

import xml.etree.ElementTree as ET
from TypeDef import TypeDef

def parse_xml(web_data):
        if len(web_data) == 0:
            return None
        xmlData = ET.fromstring(web_data)
        msg_type = xmlData.find('MsgType').text
        if msg_type == 'text':
            return TextMsg(xmlData)
        elif msg_type == 'image':
            return ImageMsg(xmlData)
        elif msg_type == "event":
            return EventMsg(xmlData)
        elif msg_type == "voice":
            return VoiceMsg(xmlData)
        else:
            pass

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text


class VoiceMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.Format = xmlData.find('Format').text
        self.MediaId = xmlData.find('MediaId').text
        self.Recognition  = xmlData.find('Recognition').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class EventMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.event = xmlData.find("Event").text
        if self.event in TypeDef.CustEvent:
            self.key_value =  xmlData.find("EventKey").text
        else:
            self.key_value = ""



class SelfEventMsg(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)

