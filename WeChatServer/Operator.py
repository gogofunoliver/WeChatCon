from UserHandler import *
from FileHandler import *
from WeatherHandler import WeatherHandler
import receive
import reply
from utill import Utill
from Resource import *
from TypeDef import TypeDef
from WeChatCon import WeChatHandler
from ActionHandler import *
class OperationType(object):

    @staticmethod
    def get_operate_function(action):
        actions = {
            TypeDef.OP_Read : Operate.read,
            TypeDef.OP_Write : Operate.write,
            TypeDef.OP_Check : Operate.check,
            TypeDef.OP_Remove : Operate.remove,
            "SubWea" : Operate.subWeather,
            TypeDef.OP_WeatherSub : Operate.subWeather,
            "Weather" : Operate.checkWeather,
            TypeDef.OP_WeatherChk : Operate.checkWeather,
            "UnsubWea" : Operate.unSubWeather,
            TypeDef.OP_WeatherUnSub : Operate.unSubWeather,
            TypeDef.OP_CheckArticle: Operate.checkArticle,
            "View" : Operate.checkArticle,
            TypeDef.OP_HistoryArticle: Operate.listHistoryArticle,
            "History":  Operate.listHistoryArticle,
            TypeDef.OP_Joke : Operate.onJoke,
            TypeDef.OP_Create_VM : Operate.onCreateVM,
            TypeDef.OP_Delete_VM : Operate.onDeleteVM,
        }
        return actions.get(action, TypeDef.Undefined)


class Operate(object):
    @staticmethod
    def check(msg, fromUser, lang):
        content = ""
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            note_set = DBHandler().select("SELECT RecoreData,Note from Notepad WHERE Open_ID = '%s'" % fromUser)
            index = 1
            for line in note_set[1]:
                content = content + str(index) + ") " + line[0].strftime("%Y-%m-%d %H:%M:%S") + " " + line[1] + "\n"
                index += 1
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    @staticmethod

    def  read(msg):
        pass

    @staticmethod
    def write(msg, fromUser, lang):
        user_handler = UserHandler()
        if len(msg.split()) == 0:
            content = Resource.getMsg("EmptyMsg")
        elif (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            if int(DBHandler().insert("INSERT into Notepad VALUES (null, '%s', null, '%s')" % (fromUser, msg))) == 1:
                content = Resource.getMsg("Recorded")
            else:
                content = Resource.getMsg("FailRecord")
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    @staticmethod
    def remove(msg, fromUser, lang):
        user_handler = UserHandler()
        if (user_handler.verify_user(fromUser) == 0):
            # Qulified User
            note_set = DBHandler().select("SELECT IND from Notepad WHERE Open_ID = '%s'" % fromUser)
            index = 1
            for line in note_set[1]:
                if msg == str(index):
                    DBHandler().delete("DELETE from Notepad where IND = '%d'" % line[0])
                index += 1
            content = Resource.getMsg("Removed")
        else:
            content = Resource.getMsg("QualifiedUser")
        return content

    #msg including city
    @staticmethod
    def subWeather(msg, fromUser, lang):
        content = ""
        size_city = len(msg.split())
        if size_city > 1:
            content = Resource.getMsg("MultiCityError")
        else:
            content = UserHandler.sub_user_for_weather(fromUser, msg, lang)
        return content

    @staticmethod
    def checkWeather(msg, fromUser, lang):
        content = ""
        city_size = len(msg.split())
        if city_size > 1:
            content = Resource.getMsg("OneCityCheck", lang)
        elif city_size == 0:
            content = Resource.getMsg("SpecifyCity", lang)
        else:
            content = UserHandler.user_check_weather(fromUser, msg, lang)
        return content

    @staticmethod
    def unSubWeather(msg, fromUser, lang):
        city_size = len(msg.split())
        if city_size > 1:
            content = Resource.getMsg("OnCitySub", lang)
        elif city_size == 0:
            content = Resource.getMsg("SpecifyCity", lang)
        else:
            content = UserHandler.unSub_Weahter(fromUser,msg, lang)
        return content

    @staticmethod
    def checkArticle(msg, fromUser, lang):
        content = ""
        if len(msg) > 0:
            digital_msg  = Utill.asDigital(msg)
            if digital_msg != -1:
                sql = "SELECT Media_ID from HistoryArticle WHERE IDX = '%s'" % digital_msg
                count = int(DBHandler().select(sql)[0])
                if count == 1:
                    media_ID = DBHandler().select(sql)[1][0][0]
                    WeChatHandler().postNewsToUser(fromUser, media_ID)
                else:
                    #media_ID = DBHandler().select("SELECT Media_ID from HistoryArticle ORDER BY RAND() LIMIT 1")[1][0][0]
                    content = Resource.getMsg("WrongNum", lang)
            else:
                content = Resource.getMsg("WrongNum", lang)
        else:
            content = Resource.getMsg("WrongNum", lang)
        return content

    @staticmethod
    def listHistoryArticle(msg, fromUser, lang):
        if lang != 'zh_CN':
            results = DBHandler().select("SELECT IDX,Title from HistoryArticle WHERE Language = 'en'")
        else:
            results = DBHandler().select("SELECT IDX,Title from HistoryArticle")

        content = Resource.getMsg("ViewCMD", lang)

        for line in results[1]:
            content = content + str(line[0]) + "..." + line[1] + "\n"
        return content

    @staticmethod
    def onJoke(msg, fromUser, lang):
        return DBHandler().select("SELECT Content from JokeList ORDER BY RAND() LIMIT 1")[1][0][0]

    @staticmethod
    def onCreateVM(msg, fromUser, lang):
        reply = ""
        if fromUser in UserHandler.openID:
            ActionsExecutor.add_auto_action(Action(Operate.onCreateVM2, fromUser, lang))
            reply = Resource.getMsg("CreateVM", lang)
        else:
            reply = Resource.getMsg("NoPermission", lang)
        return reply

    @staticmethod
    def onDeleteVM(msg, fromUser, lang):
        reply = ""
        if fromUser in UserHandler.openID:
            ActionsExecutor.add_auto_action(Action(Operate.onDeleteVM2, fromUser, lang))
            reply = Resource.getMsg("RMEC2", lang)
        else:
            reply = Resource.getMsg("NoPermission", lang)
        return reply

    @staticmethod
    def onDeleteVM2(fromUser, lang):
        print("onDeleteVM2 enter")
        delete_list = []

        vm_status = os.popen("cd /root/aws_script/terraform_sample; terraform destroy -force")
        for line in vm_status.readlines():
            if line.find("Destruction complete") != -1:
                EC2_name = line.split()[0].split(".")[1].strip(":")
                if EC2_name not in delete_list:
                    delete_list.append(EC2_name)

        if len(delete_list) > 0:
            msg = Resource.getMsg("DeletedEC2", lang) % "，".join(delete_list)
        else:
            msg = Resource.getMsg("NoInstance", lang)
        WeChatHandler().sendMsgToOneAsPreview(msg, "touser", fromUser)

    @staticmethod
    def onCreateVM2(fromUser, lang):
        print("onCreateVM2 enter")
        aws_create_vm_cmd = "/root/aws_script/terraform_sample/aws_start.sh"
        os.system(aws_create_vm_cmd)
        vm_status = os.popen("cd /root/aws_script/terraform_sample; terraform show")
        vm = {}
        for line in vm_status.readlines():
            key_value = line.split("=")
            print(key_value)
            if type(key_value) == list and len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip().strip("\n")
                vm[key] = value
        vm_status.close()

        msg = "Create VM id <%s> with AMI <%s>. Private IP <%s>, Public IP <%s>" % \
              (vm['id'], vm['ami'], vm['private_ip'], vm['public_ip'])
        print(msg)
        WeChatHandler().sendMsgToOneAsPreview(msg, "touser", fromUser)
        print("onCreateVM2 out")