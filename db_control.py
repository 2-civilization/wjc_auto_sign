import aiosqlite
import asyncio
from time import time
from datetime import datetime
from setting import DB_INIT_SQL,FAIL_MAX_TRY_DAYS
from log_setting import logger

def getTime():
    return str(time()).replace('.','')[:13]

class DBControl:
    def __init__(self, db_path):
        self.db_path = db_path

    async def init_db(self):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(DB_INIT_SQL)
        await db.commit()
        await db.close()
    
    async def add_user(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        cursor_by_account = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        cursor_by_email = await db.execute(f"SELECT * FROM users WHERE email = ?", (email,))
        if await cursor_by_account.fetchone() or await cursor_by_email.fetchone():
            logger.info(f"添加或更新用户{account} 添加成功")
            await db.close()
            return await self.update_user(account, pswd, email, coordinate)
        else:
            await db.execute(f"INSERT INTO users (id,pswd,email,coordinate,updateTime,signTime,success,total,active) VALUES (?,?,?,?,?,?,?,?,?)", (account, pswd, email, coordinate, getTime(), 0, 0, 0,1))
            await db.commit()
            await db.close()
            logger.info(f"添加或更新用户{account} 添加成功")
    
    async def check_user(self, account):
        """
        检查用户是否签到

        """
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
            return {'code':'fail','msg':'用户不存在','info':None}
    
    async def __update_user_by_account(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"UPDATE users SET pswd=?,email=?,coordinate=?,updateTime=?,failDays=0,active=1 WHERE id = ?", (pswd, email, coordinate,getTime(),account))
        await db.commit()
        await db.close()

    async def __update_user_by_email(self, account, pswd, email, coordinate):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"UPDATE users SET id=?,pswd=?,coordinate=?,updateTime=?,failDays=0,active=1 WHERE email=?", (account,pswd,coordinate,getTime(),email))
        await db.commit()
        await db.close()

    async def update_user(self, account, pswd, email, coordinate):
        """
        附带账号检查的账号更新

        若账号可查询，则以账号更新优先，更新剩余数据；若账号不可查，则以邮箱优先，更新剩余数据。
        传入数据至少要做到邮箱准确可查
        
        :param account: 账号
        :param pswd: 密码
        :param email: 邮箱
        :param coordinate: 签到坐标
        :return: None
        """
        db = await aiosqlite.connect(self.db_path)
        cursor_by_account = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        cursor_by_email = await db.execute(f"SELECT * FROM users WHERE email = ?", (email,))
    
        if await cursor_by_account.fetchone():
            db.close()
            await self.__update_user_by_account(account, pswd, email, coordinate)
            logger.info(f"更新用户{account}信息成功[账号优先 {account}]")
            return {'code':'ok','msg':f"更新用户{account}信息成功[账号优先 {account}]"}
        elif await cursor_by_email.fetchone():
            db.close()
            await self.__update_user_by_email(account,pswd,email,coordinate)
            logger.info(f"更新用户{account}信息成功[邮箱优先 {email}]")
            return {'code':'ok','msg':f"更新用户{account}信息成功[邮箱优先 {email}]"}
        else:
            db.close()
            logger.info(f"更新用户{account}信息失败[账号或邮箱不存在 {email}]")
            return {'code':'fail','msg':f"更新用户{account}信息失败[账号或邮箱不存在 {email}]"}


    async def user_try_add(self,account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT total FROM users WHERE id = ?", (account,))
        sign_info = await cursor.fetchone()
        cursor = await db.execute(f"UPDATE users SET total=? WHERE id = ?", (sign_info[0]+1,account))
        await db.commit()
        await db.close()
        logger.info(f"更新用户{account}签到次数成功")
        return {'code':'ok','msg':f"更新用户{account}签到次数成功"}

    async def user_sign(self, account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT success,total FROM users WHERE id = ?", (account,))
        sign_info = await cursor.fetchone()
        cursor = await db.execute(f"UPDATE users SET signTime=?,success=?,total=? WHERE id = ?", (getTime(),sign_info[0]+1,sign_info[1]+1,account))
        await db.commit()
        await db.close()
        logger.info(f"更新用户{account}签到状态成功")
        return {'code':'ok','msg':f"更新用户{account}签到状态成功"}
    
    async def get_users_info(self):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users")
        users_info = await cursor.fetchall()
        await db.close()
        return users_info
    
    async def deactive_user(self,account) -> bool:
        '''
        申请对签到失败的用户，将其停用

        会自动判断是否符合禁用条件并做出相应的处理。
        :param account: 用户账号
        :return: 如果符合禁用条件，将会禁用并返回True，否则返回False
        '''
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM users WHERE id = ?", (account,))
        user_info = await cursor.fetchone()
        if user_info[9]>=FAIL_MAX_TRY_DAYS:
            await db.execute(f"UPDATE users SET active=? WHERE id = ?", (0,account))
            await db.commit()
            logger.info(f"由于连续签到失败，用户{account}被禁用")
            await db.close()
            return True
        else:
            await db.close()
            return False
        
    async def user_fail_day_add(self,account):
        db = await aiosqlite.connect(self.db_path)
        cursor = await db.execute(f"SELECT failDays FROM users WHERE id = ?", (account,))
        fail_day = await cursor.fetchone()
        cursor = await db.execute(f"UPDATE users SET failDays=? WHERE id = ?", (fail_day[0]+1,account))
        logger.info(f"用户{account}连续签到失败{fail_day[0]+1}天")
        await db.commit()
        await db.close()
    
    async def reset_fail_day(self,account):
        db = await aiosqlite.connect(self.db_path)
        await db.execute(f"UPDATE users SET failDays=0 WHERE id = ?", (account))
        logger.info(f"重置用户{account}连续签到失败天数")
        await db.commit()
        await db.close()

async def getDBControl(db_path):
    DB = DBControl(db_path)
    await DB.init_db()
    return DB


