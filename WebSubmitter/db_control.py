import aiosqlite
import asyncio
from time import time
from datetime import datetime
from setting import logger

def getTime():
    return str(time()).replace('.','')[:13]

class DBControl:
    def __init__(self, db_path):
        self.db_path = db_path
        asyncio.run(self.__init_db())
    

    async def __init_db(self):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL,pswd TEXT NOT NULL,email TEXT NOT NULL,coordinate TEXT NOT NULL,updateTime TEXT,signTime TEXT,success INTEGER,total INTEGER)")
        await db.commit()
        await db.close()
    
    async def add_user(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        if await cursor.fetchone():
            return await self.update_user(account, pswd, email, coordinate)
        else:
            await db.execute(f"INSERT INTO users (id,pswd,email,coordinate,updateTime,signTime,success,total) VALUES (?,?,?,?,?,?,?,?)", (account, pswd, email, coordinate, getTime(), 0, 0, 0))
            await db.commit()
    
    async def check_user(self, account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        if await cursor.fetchone():
            user_info = await cursor.fetchone()
            lastSignTime = datetime.fromtimestamp(int(user_info[5]) / 1000.0).date()
            now_time = datetime.now(datetime.timezone.utc).date()
            if lastSignTime == now_time:
                return {'code':0,'msg':'该用户已经签到','info':user_info}
            else:
                return {'code':1,'msg':'该用户未签到','info':user_info}
        else:
            return {'code':-1,'msg':'用户不存在'}
    
    async def update_user(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"UPDATE users SET pswd=?,email=?,coordinate=?,updateTime=? WHERE id = ?", (pswd, email, coordinate,getTime(),account))
        await db.commit()

    async def user_sign(self, account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT success,total FROM users WHERE id = ?", (account,))
        sign_info = await cursor.fetchone()
        cursor = await db.execute(f"UPDATE users SET signTime=?,success=?,total=? WHERE id = ?", (getTime(),sign_info[0]+1,sign_info[1]+1,account))
        await db.commit()
        await db.close()
        return {'code':0,'msg':'签到成功'}
    
    async def get_users_info(self):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users")
        users_info = await cursor.fetchall()
        await db.close()
        return users_info
    
    
