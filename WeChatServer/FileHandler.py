import sys, io, os
import time
import codecs

class Record(object):
    def __init__(self, msg):
        self.local_time = time.strftime('%Y-%m-%d@@%H:%M:%S', time.localtime(time.time()))
        self.msg = msg

class FileHandler(object):
    def __init__(self, user):
        self.index = 0
        self.__data__ = "/wechat/data/" + user + ".data"
        if os.path.exists(self.__data__):
            self.index = int(os.popen("tail -n 1 " + self.__data__ + " |awk -F#@# '{print $1}'").read())
            self.index +=1
            print("Index: {0}".format(self.index))
        else:
            file_handler = codecs.open(self.__data__, "w")
            try:
                pass
            except Exception as Ex:
                print("Error in FileHandler.__init__")
            finally:
                file_handler.close()

    def add_record(self, msg):
        local_time = time.strftime('%Y-%m-%d#@#%H:%M:%S', time.localtime(time.time()))
        appender = codecs.open(self.__data__, 'a+', 'utf-8')
        line = '%d'%self.index + "#@#" + local_time + "##@@##" + msg + "\n"
        appender.write(line)
        appender.close()


    def read_all_record(self):
        file_handler = codecs.open(self.__data__, 'r', 'utf-8')
        all_text = file_handler.read()
        file_handler.close()
        all_text = all_text.replace("#@#", " ")
        all_text = all_text.replace("##@@##", "\t")
        return all_text

    def remove_record(self, key):
        pass
