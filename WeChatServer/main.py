 # -*- coding: utf-8 -*-
# filename: main.py
import web
from ServerEntry import Handle

#Sepcify the rest api with a handler
urls = (
    '/wx', 'Handle',
)

urls = (
    '/wx', 'Handle',
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
