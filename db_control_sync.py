import sqlite3
from time import time
from datetime import datetime
from setting import logger,DB_INIT_SQL

def getTime():
    return str(time()).replace('.','')[:13]

class DBControl:
    def __init__(self, db_path):
        self.db_path = db_path
        self.__init_db()
    

    def __init_db(self):
        db = sqlite3.connect(self.db_path)
        db.execute(DB_INIT_SQL)
        db.commit()
        db.close()
    
    def add_user(self, account, pswd, email, coordinate):
        db = sqlite3.connect(self.db_path)
        cursor = db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        if cursor.fetchone():
            return self.update_user(account, pswd, email, coordinate)
        else:
            db.execute(f"INSERT INTO users (id,pswd,email,coordinate,updateTime,signTime,success,total) VALUES (?,?,?,?,?,?,?,?)", (account, pswd, email, coordinate, getTime(), 0, 0, 0))
            db.commit()
    
    def check_user(self, account):
        db = sqlite3.connect(self.db_path)
        cursor =db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        if cursor.fetchone():
            user_info =  cursor.fetchone()
            lastSignTime = datetime.fromtimestamp(int(user_info[5]) / 1000.0).date()
            now_time = datetime.now(datetime.timezone.utc).date()
            if lastSignTime == now_time:
                return {'code':0,'msg':'该用户已经签到','info':user_info}
            else:
                return {'code':1,'msg':'该用户未签到','info':user_info}
        else:
            return {'code':-1,'msg':'用户不存在'}
    
    def update_user(self, account, pswd, email, coordinate):
        db =  sqlite3.connect(self.db_path)
        db.execute(f"UPDATE users SET pswd=?,email=?,coordinate=?,updateTime=? WHERE id = ?", (pswd, email, coordinate,getTime(),account))
        db.commit()

    def user_sign(self, account):
        db =  sqlite3.connect(self.db_path)
        cursor =  db.execute(f"SELECT success,total FROM users WHERE id = ?", (account,))
        sign_info =  cursor.fetchone()
        cursor =  db.execute(f"UPDATE users SET signTime=?,success=?,total=? WHERE id = ?", (getTime(),sign_info[0]+1,sign_info[1]+1,account))
        db.commit()
        db.close()
        return {'code':0,'msg':'签到成功'}
    
    def get_users_info(self):
        db =  sqlite3.connect(self.db_path)
        cursor =  db.execute(f"SELECT * FROM users")
        users_info =  cursor.fetchall()
        db.close()
        return users_info
    
    
