'''
DB 数据迁移
1.0.X迁移至1.1.X
'''

import aiosqlite
import asyncio

SOURCE_DB = 'source.db'
TARGET_DB = 'target.db'

async def init_db():
    DB_INIT_SQL = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY,
        pswd TEXT NOT NULL,
        email TEXT NOT NULL,
        coordinate TEXT NOT NULL,
        updateTime TEXT NOT NULL,
        signTime TEXT,
        success INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1,
        failDays INTEGER DEFAULT 0
    );
'''
    db = await aiosqlite.connect(TARGET_DB)
    await db.execute(DB_INIT_SQL)
    await db.commit()
    await db.close()

async def start():
    
    source_db = await aiosqlite.connect(SOURCE_DB)
    datas = await source_db.execute_fetchall('select * from users')
    await source_db.close()

    await init_db()
    target_db = await aiosqlite.connect(TARGET_DB)
    for data in datas:
        await target_db.execute('insert into users (id,pswd,email,coordinate,updateTime,signTime,success,total) values (?,?,?,?,?,?,?,?)',data)
    await target_db.commit()
    await target_db.close()
    print('done')

if __name__ == '__main__':
    asyncio.run(start())
