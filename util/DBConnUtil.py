from Ecom.util.DBPropertyUtil import PropertyUtil

import mysql.connector as sql


class DbConnect():
    def __init__(self):
        self.conn = None
        self.stmt = None
        pass

    def open(self):
        try:
            l = PropertyUtil.getPropertyString()
            self.conn = sql.connect(host=l[0], database=l[3], username=l[1], password=l[2])
            if self.conn:
                print("--Database Is Connected--")
            self.stmt = self.conn.cursor()
        except Exception as e:
            print(e)

    def close(self):
        self.conn.close()
