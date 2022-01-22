from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("progress", "Прогресс перехода на новый движок"),
        types.BotCommand("me", "Краткая сводка по тебе 🏅"),
        types.BotCommand("help", "Помощь ❓"),
        types.BotCommand("mob", "Симулятор боя с мобами 👹"),
        types.BotCommand("get_user", "Пробить игрока по базе бота 🔍"),
        types.BotCommand("cave", "Показать пещерныйх людей 🚠"),
        types.BotCommand("boosters", "Усиление персонажа, краткая сводка (доступно с 51 лвл)"),
        types.BotCommand("find_contract", "Найти контракт 👷‍♀️(доступно с 38 лвл)"),
        types.BotCommand("totems", "Сводка по тотетам 🗿"),
        types.BotCommand("config", "Найстройки⚙️(уведомления/чат)"),
        types.BotCommand("item", "Сверить скрафченный предмет с базой"),
        types.BotCommand("ping_guild", "Пингануть гильдию [admins chat only]"),
        types.BotCommand("get_guild", "Получить состав гильдии"),
        types.BotCommand("cave_pin", "Ты знаешь для чего эта команда😎"),
    ])
    await dp.bot.set_my_commands([
        types.BotCommand("progress", "Прогресс перехода на новый движок"),
        types.BotCommand("me", "Краткая сводка по тебе 🏅"),
        types.BotCommand("help", "Помощь ❓"),
        types.BotCommand("mob", "Симулятор боя с мобами 👹"),
        types.BotCommand("get_user", "Пробить игрока по базе бота 🔍"),
        types.BotCommand("cave", "Показать пещерныйх людей 🚠"),
        types.BotCommand("boosters", "Усиление персонажа, краткая сводка (доступно с 51 лвл)"),
        types.BotCommand("find_contract", "Найти контракт 👷‍♀️(доступно с 38 лвл)"),
        types.BotCommand("totems", "Сводка по тотетам 🗿"),
        types.BotCommand("config", "Найстройки⚙️(уведомления/чат)"),
        types.BotCommand("item", "Сверить скрафченный предмет с базой"),
        types.BotCommand("ping_guild", "Пингануть гильдию [admins chat only]"),
        types.BotCommand("get_guild", "Получить состав гильдии"),
        types.BotCommand("cave_pin", "Ты знаешь для чего эта команда😎"),
    ])
