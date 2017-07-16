import pymysql.cursors
from time import sleep

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
        pass

    def delete(self, sql):
        pass

    def insert(self, sql):
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
    db = DBHandler()
    sql = "SELECT * FROM HealthyRecord WHERE ID = 2 "
    result = db.select(sql)
    lines = result[0]
    rows = result[1]
    print("lines : %s" % lines)
    for row in rows:
        print("ID:%d\tSOpen_ID:%s\tContent:%s\tDataStr:%s" % row)
'''