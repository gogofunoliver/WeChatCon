 # -*- coding: utf-8 -*-
# filename: main.py
import web
from ServerEntry import Handle
from ThreadPool import *

#Sepcify the rest api with a handler
urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    WechatRefresher.start()
    sleep(2) #wait wechat token refresh
    #other threads
    #send weather to  subscriber
    ThreadPool.get_instance().add_thread(PublisherToSub.run, "Publiser")
    ThreadPool.get_instance().run_threads()
    #web
    app = web.application(urls, globals())
    app.run()
