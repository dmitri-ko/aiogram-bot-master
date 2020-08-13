from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("info ", "Посмотреть информацию о текущем сезоне"),
        types.BotCommand("standings", "Просмотреть турнирную таблицу"),
        types.BotCommand("fixtures", "Просмотреть расписание предстоящих туров"),
        types.BotCommand("results", "Посмотреть результаты прошедших матчей"),
    ])
