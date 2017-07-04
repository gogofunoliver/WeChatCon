from UserHandler import *
from FileHandler import *
import receive
import reply

class OperationType(object):
    Read = 1
    Write = 2
    Check = 3
    Remove = 4
    UnDefined = 5

    @staticmethod
    def get_operate_type(action):
        actions = {
            "查询" : OperationType.Read,
            "记录" : OperationType.Write,
            "查询" : OperationType.Check,
            "删除" : OperationType.Remove,
        }
        return actions.get(action, OperationType.UnDefined)

    @staticmethod
    def get_operate_function(action):
        actions = {
            OperationType.Read : Operate.read,
            OperationType.Write : Operate.write,
            OperationType.Check : Operate.check,
            OperationType.Remove : Operate.remove,
        }
        return actions.get(action, OperationType.UnDefined)


class Operate(object):
    @staticmethod
    def check(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            content = file_handler.read_all_record()
        else:
            content = "你不是马**或怼她的人，没权限使用记录和提醒功能"
        return content

    @staticmethod
    def  read(msg):
        pass

    @staticmethod
    def write(msg, fromUser):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            file_handler = FileHandler(fromUser)
            file_handler.add_record(msg)
            content = "已记录"
        else:
            content = "你不是马**或怼她的人，没权限使用记录和提醒功能"
        return content

    @staticmethod
    def remove(msg):
        pass

