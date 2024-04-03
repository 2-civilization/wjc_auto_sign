import aiosqlite
import asyncio
from time import time
from datetime import datetime
from setting import logger,DB_INIT_SQL

def getTime():
    return str(time()).replace('.','')[:13]

class DBControl:
    def __init__(self, db_path):
        self.db_path = db_path
        asyncio.run(self.__init_db())
    

    async def __init_db(self):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(DB_INIT_SQL)
        await db.commit()
        await db.close()
    
    async def add_user(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        if await cursor.fetchone():
            logger.info(f"添加或更新用户{account} 添加成功")
            await db.close()
            return await self.update_user(account, pswd, email, coordinate)
        else:

            await db.execute(f"INSERT INTO users (id,pswd,email,coordinate,updateTime,signTime,success,total) VALUES (?,?,?,?,?,?,?,?)", (account, pswd, email, coordinate, getTime(), 0, 0, 0))
            await db.commit()
            await db.close()
            logger.info(f"添加或更新用户{account} 添加成功")
    
    async def check_user(self, account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        user_info = await cursor.fetchone()
        if user_info:
            lastSignTime = datetime.fromtimestamp(int(user_info[5]) / 1000.0).date()
            now_time = datetime.now().date()
            await db.close()
            if lastSignTime == now_time:
                return {'code':'ok_signed','msg':'该用户已经签到','info':user_info}
            else:
                return {'code':'ok','msg':'该用户未签到','info':user_info}
        else:
            await db.close()
            return {'code':'fail','msg':'用户不存在'}
    
    async def update_user(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"UPDATE users SET pswd=?,email=?,coordinate=?,updateTime=? WHERE id = ?", (pswd, email, coordinate,getTime(),account))
        await db.commit()
        await db.close()

    async def user_sign(self, account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT success,total FROM users WHERE id = ?", (account,))
        sign_info = await cursor.fetchone()
        cursor = await db.execute(f"UPDATE users SET signTime=?,success=?,total=? WHERE id = ?", (getTime(),sign_info[0]+1,sign_info[1]+1,account))
        await db.commit()
        await db.close()
        logger.info(f"更新用户{account}签到状态成功")
        return {'code':'ok','msg':'签到成功'}
    
    async def get_users_info(self):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users")
        users_info = await cursor.fetchall()
        await db.close()
        return users_info
    
    
