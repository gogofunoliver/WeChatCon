# -*- coding: utf-8 -*-
# filename: main.py
import web
import utill
from ServerEntry import *
from AWSHandler import AWSHandler
from ThreadPool import *
from HealthyNotifier import HealthyNotifier
from BirthDayNotifier import BirthDayNotifier
from ActionHandler import  *
from WeChatCon import WechatRefresher

#Sepcify the rest api with a handler
urls = (
    '/wx', 'Handle',
    '/aws', 'AWSHandler'
)

if __name__ == '__main__':
    #init log
    utill.Utill.log_init()

    WechatRefresher.start()
    sleep(2)
    #wait wechat token refresh

    #other threads
    #send weather to  subscriber
    #ThreadPool.get_instance().add_thread("WeatherPublisher", PublisherToSub.run, "WeatherPublisher")
    #ThreadPool.get_instance().add_thread("HealthyNotifier", HealthyNotifier.get_instance().run)
    #ThreadPool.get_instance().add_thread("BirthNotifier", BirthDayNotifier().run, "Birth")

    ThreadPool.get_instance().add_thread("ActionExecutor", ActionsExecutor.run)
    ThreadPool.get_instance().run_threads()

    #ActionsExecutor.add_auto_action(Action(WeChatHandler().getAllNewsIntoDB))
    #web
    app = web.application(urls, globals())
    app.run()
