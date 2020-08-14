import logging
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from loader import dp
from utils.misc import di
from keyboards.inline import info_menu, info_callback


@dp.message_handler(Command("info"))
async def get_season_info(message: message):
    reply_msg: str = ""
    try:
        season: str = f"({di.start_date[-2:]}-{di.end_date[-2:]})"
        reply_msg = "\n".join(
            [
                hbold(f"{di.name} сезон {season}"),
                f"Период проведения с {di.start_date} по {di.end_date}. Ближайший тур: {di.match_day}",
                " Выберите, что желаете посмотреть:",
            ]
        )
        await message.answer(reply_msg, reply_markup=info_menu)
    except Exception as e:
        logging.exception(f"Ошибка при формировании результата: {repr(e)}")
        await message.answer("Сервис временно недоступен", reply_markup=ReplyKeyboardRemove())

   
