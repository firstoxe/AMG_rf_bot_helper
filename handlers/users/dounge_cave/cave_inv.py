from aiogram import types

from filters.guild_check import check_g
from keyboards.inline.cave_invite import create_cb_cave_lvl
from keyboards.inline.dounge_invite import create_cb_dounge_lvl
from loader import dp, db
from aiogram.utils.emoji import emojize, demojize
from utils.misc import rate_limit
from asyncpg import Connection, Record


leg = [
    '40-44', '45-48', '49-49', '50-50', '51-52',
    '53-54', '55-55', '56-57', '58-59', '60-60'
]


@rate_limit(2, 'create_dounge_cave')
@dp.message_handler(is_from_rf_bot=True, text_contains='Чтобы другой участник присоединился к группе перешли ему эту команду /group_guild_join_')
async def dounge_cave_cr_inv(message: types.Message):
    pool: Connection = db
    find_user: Record = await pool.fetchrow('''SELECT * FROM test.public."user" WHERE id = $1''', message.from_user.id,)
    if find_user:
        usr_leg = ''
        for item in leg:
            if int(item.split('-')[0]) >= find_user["lvl"]:
                if int(item.split('-')[1]) <= int(item.split('-')[1]):
                    usr_leg = item
                    break
        await message.reply((f'Привет {check_g(find_user["guild"])}{emojize(find_user["nickname"])}\n'
                             f'Ты создал группу в 🚠пещеру для лиги 🏅{usr_leg}'),
                            reply_markup=await create_cb_cave_lvl(
                                find_user["id"],
                                usr_leg,
                                cave_id=message.text.split('/group_guild_join_')[1]
                            )
                            )
