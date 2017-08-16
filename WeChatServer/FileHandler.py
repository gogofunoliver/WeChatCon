import sys, io, os
import time
import codecs


class Record(object):
    def __init__(self, msg):
        self.local_time = time.strftime('%Y-%m-%d@@%H:%M:%S', time.localtime(time.time()))
        self.msg = msg


class FileHandler(object):
    def __init__(self, user):
        self.__data__ = "/wechat/data/" + user + ".data"
        if os.path.exists(self.__data__):
            pass
        else:
            file_handler = codecs.open(self.__data__, "w")
            try:
                pass
            except Exception as Ex:
                print("Error in FileHandler.__init__")
            finally:
                file_handler.close()

    @staticmethod
    def create_file_if_no(file_path):
        ret = 0
        if os.path.exists(file_path):
            pass
        else:
            file_handler = codecs.open(file_path, "w")
            file_handler.close()
            ret = 1
        return ret

    def add_record(self, msg):
        local_time = time.strftime('%Y-%m-%d#@#%H:%M:%S', time.localtime(time.time()))
        appender = codecs.open(self.__data__, 'a+', 'utf-8')
        line = local_time + "##@@##" + msg + "\n"
        appender.write(line)
        appender.close()


    def read_all_record(self):
        file_handler = codecs.open(self.__data__, 'r', 'utf-8')
        index = 1
        ret_text = ""
        for line in file_handler.readlines():
            line = str(index) + ": " + line
            ret_text += line
            index+=1
        file_handler.close()

        ret_text = ret_text.replace("#@#", " ")
        ret_text = ret_text.replace("##@@##", "\t")
        return ret_text

    def remove_record(self, key):
        file_handler = codecs.open(self.__data__, 'r', 'utf-8')
        index = 1
        new_text = ""
        for line in file_handler.readlines():
            if index == int(key):
                index += 1
                continue

            new_text += line
            index += 1
        file_handler.close()

        file_handler = codecs.open(self.__data__, 'w', 'utf-8')

        file_handler.write(new_text)
        file_handler.close()





