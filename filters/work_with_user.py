from aiogram import types
from loader import db
from asyncpg import Record, Connection
from aiogram.utils.emoji import emojize


async def helper_user(id, action='guild_nick_link'):
    pool: Connection = db
    user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', id,)
    if Record:
        if user["nickname"]:
            if action == 'nick':
                return emojize(user["nickname"])
            if action == 'guild':
                if user["guild"]:
                    return f'[{emojize(user["guild"])}]'
                else:
                    return ''
            if action == 'guild_nick':
                if user["guild"]:
                    return f'[{emojize(user["guild"])}]{emojize(user["nickname"])}'
                else:
                    return f'{emojize(user["nickname"])}'
            if action == 'nick_link':
                return f"<a href='tg://user?id={id}'>{emojize(user['nickname'])}</a>"
            if action == 'guild_nick_link':
                if user["guild"]:
                    return f"[{emojize(user['guild'])}]<a href='tg://user?id={id}'>{emojize(user['nickname'])}</a>"
                else:
                    return f"<a href='tg://user?id={id}'>{emojize(user['nickname'])}</a>"
        else:
            return ''
    else:
        return ''
