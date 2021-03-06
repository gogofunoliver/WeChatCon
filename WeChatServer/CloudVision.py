# -*- coding: utf-8 -*-
# filename: CloudVision.py
# Jason Li
# text detection API

import argparse
import io

from google.cloud import vision
from google.cloud.vision import types

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


