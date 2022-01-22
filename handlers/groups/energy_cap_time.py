from aiogram import types
from loader import dp, db
from datetime import datetime, timedelta
from asyncpg import Connection, Record
from utils.misc import rate_limit


@rate_limit(3, 'msg_energy_cap')
@dp.message_handler(is_from_rf_bot=True, is_energy_cap=True)
async def bot_msg_energy_cap(message: types.Message):
    pool: Connection = db
    prem: Record = await pool.fetchval(f"""SELECT premium from test.public.user where id = {message.from_user.id}""")

    if message.text.find('5/5') != -1:
        await message.answer('🔋 макс! 6 ещё не добавили =)')
    else:
        enk = int(message.text[-3])
        schet = 1
        result_aws = []
        dt_now = datetime.now()

        def anws_without_prem(schet1, enk1, result_aws1):
            anws = f'+{schet1} к🔋{enk1+1}/5 в {(message.forward_date + timedelta(minutes=25 * schet)).time()} ≈ '
            if message.forward_date + timedelta(minutes=25 * schet) - dt_now > timedelta(seconds=0):
                result_aws1.append(f'{anws}'
                                   f'{str(message.forward_date + timedelta(minutes=25 * schet) - dt_now).split(".")[0]}')
            else:
                result_aws1.append(f'{anws}кап')
            return result_aws1
        
        while enk != 7:
            if prem:
                if message.forward_date.date() < prem:
                    aws = (f'+{schet} к🔋{enk+1}/5 в '
                           f'{(message.forward_date + timedelta(minutes=17 * schet, seconds=30 * schet)).time()} ≈ ')
                    if message.forward_date + timedelta(minutes=17 * schet, seconds=30 * schet) - dt_now \
                            > timedelta(seconds=0):
                        result_aws.append(f'{aws}'
                                          f'{str(message.forward_date + timedelta(minutes=17 * schet, seconds=30 * schet) - dt_now).split(".")[0]}')
                    else:
                        result_aws.append(f'{aws}кап')
                else:
                    result_aws = anws_without_prem(schet, enk, result_aws)
            elif not prem:
                result_aws = anws_without_prem(schet, enk, result_aws)
            if enk == 4:
                result_aws.append('')
            schet += 1
            enk += 1
        await message.answer('\n'.join(result_aws))
