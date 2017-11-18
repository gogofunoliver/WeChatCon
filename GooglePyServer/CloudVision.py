# -*- coding: utf-8 -*-
# filename: CloudVision.py
# Jason Li
# text detection API

import argparse
import io

from google.cloud import vision
from google.cloud.vision import types


<<<<<<< HEAD
class GCPCV(object):

    def detect_document(path):
        """Detects document features in an image."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
                content = image_file.read()

        image = types.Image(content=content)

        response = client.document_text_detection(image=image)
        document = response.full_text_annotation

        for page in document.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)

                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)

                block_text = ''
                for symbol in block_symbols:
                    block_text = block_text + symbol.text

                print('Block Content: {}'.format(block_text))
                print('Block Bounds:\n {}'.format(block.bounding_box))


    def callGCPCV(path):
        """called from wechat """
        content = ""
        try:
            saveIMG = "/tmp/aws_tmp_image.img"
            saveReplyFile = "/tmp/aws_reply_image.img"

        # 1. Get WeChat IMG
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
        except
            Exception as ex:
            traceback.print_exc()
        finally:
            print(content)
            return content

=======

def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
>>>>>>> origin/master
