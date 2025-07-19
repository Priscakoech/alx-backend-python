import asyncio
import aiosqlite

async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            return await cursor.fetchall()
async def async_fetch_older_users(db_name, age):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users WHERE age > ?', (age,)) as cursor:
            return await cursor.fetchall()
async def fetch_concurrently(db_name):
    users_task = async_fetch_users(db_name)
    older_users_task = async_fetch_older_users(db_name, 40)
    users, older_users = await asyncio.gather(users_task, older_users_task)
    return users, older_users
if __name__ == "__main__":
    db_name = 'example.db'
    
    async def setup_db():
        async with aiosqlite.connect(db_name) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
            await db.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
            await db.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 50))
            await db.commit()
    asyncio.run(setup_db())
    
    # Run the concurrent fetch
    users, older_users = asyncio.run(fetch_concurrently(db_name))
    print("All Users:", users)
    print("Users older than 40:", older_users)
    