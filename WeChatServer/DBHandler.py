 # -*- coding: utf-8 -*-
# filename: DBHanlder.py

import pymysql.cursors
from time import sleep
from Resource import Resource

class DBHandler(object):
    def __init__(self):
        self.connection = pymysql.Connect(
            host='123.207.172.207',
            port=3306,
            user='gogofun',
            passwd='gogofun',
            db='gogofun',
            charset='utf8'
        )
        self.cursor = self.connection.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        affected_lines = self.cursor.rowcount
        self.close()
        return (affected_lines, rows);

    def update(self, sql):
        return self.write_db(sql)

    def delete(self, sql):
        return self.write_db(sql)

    def insert(self, sql):
        return self.write_db(sql)

    def write_db(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()
        affected_lines = self.cursor.rowcount
        self.close()
        return affected_lines

    def close(self):
        print("Deconstruct")
        self.cursor.close()
        self.connection.close()

'''
if __name__ == "__main__":
    user = 'oHBF6wR4kUe4KUNtMMN4J0LKXsPE'
    counts = DBHandler().select("SELECT CreateData from HealthyRecord WHERE IsRecord = 'Y' and CreateData > '2017-07' \
    and CreateData < '2017-08' AND Open_ID = '%s'" % user)[0]
    content = Resource.getMsg("RecordFmt") % (Resource.getMsg("LingSub"), str(counts))
    print(content)
'''