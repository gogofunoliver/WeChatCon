 # -*- coding: utf-8 -*-
# filename: ActionHandler.py
from time import sleep
import threading
import logging

class Action(object):
    def __del__(self):
        print("des action")

    def __init__(self, func,  *arg):
        self.func = func
        self.para = arg

    def execute(self):
        return self.func(*self.para)

    def execute_with_arg(self, *arg):
        return self.func(*arg)


class ActionsExecutor(object):
    auto_actions_handlers = []
    manual_action_handlers = {"" : [] }
    logger = logging.getLogger("root.ActionHandler")

    @staticmethod
    def add_auto_action(fun_action):
        ActionsExecutor.auto_actions_handlers.append(fun_action)
        ActionsExecutor.logger.info("added an auto-action")


    def add_manual_action(user, fun_action):
        old_actions = ActionsExecutor.manual_action_handlers.get(user, "no")
        if type(old_actions) == list and len(old_actions) != 0:
            old_actions.append(fun_action)
            ActionsExecutor.manual_action_handlers[user] = old_actions
        else:
            ActionsExecutor.manual_action_handlers[user] = [ fun_action ]
            ActionsExecutor.logger.info("added a manual action")

    @staticmethod
    def has_manual_actions(user):
        ret = 0
        actions = ActionsExecutor.manual_action_handlers.get(user, "no")
        if type(actions) == list and len(actions) > 0:
            ActionsExecutor.logger.info("has manual action")
            ret = 1
        return ret

    @staticmethod
    def exuecte_actions(user, para):
        actions = ActionsExecutor.manual_action_handlers.get(user, "no")
        while type(actions) == list and len(actions) > 0:
            # FIFS
            action = actions.pop(0)
            ActionsExecutor.logger.info("execute action with para: %s" % para)
            return action.execute_with_arg(user, para)

    @staticmethod
    def run():
        ActionsExecutor.logger.info("Start Action Handler")
        while(1):
            while type(ActionsExecutor.auto_actions_handlers) == list and len(ActionsExecutor.auto_actions_handlers) > 0:
                #FIFS
                action = ActionsExecutor.auto_actions_handlers.pop(0)
                ActionsExecutor.logger.info("Get an auto-action. Executing...")
                action.execute()
            sleep(2)

            #empty list, need remove from the dict to save mem. thread-safe need consider

