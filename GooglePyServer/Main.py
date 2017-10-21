 # -*- coding: utf-8 -*-
# filename: Main.py
import web
from LexConnector import LexConnector
from GoogleHanlder import GoogleHanlder

#Sepcify the rest api with a handler
urls = (
    '/google', 'GoogleHanlder',
    '/lexcon', 'LexConnector'
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()