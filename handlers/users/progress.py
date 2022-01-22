from aiogram import types
from loader import dp, db
from asyncpg import Connection, Record
from aiogram.utils.emoji import emojize
from utils.misc import rate_limit


@rate_limit(5, 'progress')
@dp.message_handler(commands='progress')
async def bot_command_get_user(message: types.Message):
    await message.answer(emojize("""Прогресс перехода на новый движок:
    
:mountain_cableway:Пещеры: [********==] (уведомления о пвп, свободном пути, координация по комнатам)
:moai:Тотемы: [**********] (обновлено до 11 лвл)
:gear:Настройки: [****======]
:scroll:Рецепты: [**********](не добавлены альтернатиные имена и шорткаты)
:sports_medal:Обновление профиля [*********=](не добавлены профы и учёт бонуса к адене для /mob)
:man_detective_2:Отслеживание игроков [*********=](база актуальна с 1 августа, не добавлено отслежние по нахождению в ги)
"""))