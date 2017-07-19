 # -*- coding: utf-8 -*-
# filename: main.py
import web
from ServerEntry import Handle
from AWSHandler import AWSHandler
from ThreadPool import *
from HealthyNotifier import HealthyNotifier
from BirthDayNotifier import BirthDayNotifier
from ActionHandler import  ActionsExecutor

#Sepcify the rest api with a handler
urls = (
    '/wx', 'Handle',
    '/aws', 'AWSHandler'
)

if __name__ == '__main__':
    WechatRefresher.start()
    sleep(2) #wait wechat token refresh

    #other threads
    #send weather to  subscriber
    ThreadPool.get_instance().add_thread("WeatherPublisher", PublisherToSub.run, "WeatherPublisher")
    ThreadPool.get_instance().add_thread("HealthyNotifier", HealthyNotifier.get_instance().run)
    ThreadPool.get_instance().add_thread("BirthNotifier", BirthDayNotifier().run, "Birth")
    ThreadPool.get_instance().add_thread("ActionExecutor", ActionsExecutor().run, "ActionExecutor")
    ThreadPool.get_instance().run_threads()

    #web
    app = web.application(urls, globals())
    app.run()
