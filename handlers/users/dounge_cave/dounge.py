from aiogram import types

from filters.guild_check import check_g
from keyboards.inline.dounge_invite import create_cb_dounge_lvl
from loader import dp, db
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


@rate_limit(2, 'create_dounge')
@dp.message_handler(is_from_rf_bot=True, text_contains='Ты создал группу. Чтобы другой участник присоединился к группе перешли ему эту команду /group_join_')
async def dounge_cr_inv(message: types.Message):
    pool: Connection = db
    find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', message.from_user.id,)
    if find_user:
        await message.reply(f'Привет {check_g(find_user["guild"])}{emojize(find_user["nickname"])}\nУкажи 🏅ур. данжа🎭',
                            reply_markup=await create_cb_dounge_lvl(
                                find_user["id"],
                                find_user["lvl"],
                                dounge_id=message.text.split('/group_join_')[1]
                            )
                            )
