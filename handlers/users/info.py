import logging
from datetime import datetime

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hitalic, hunderline

from keyboards.inline import info_menu, info_menu_full
from loader import dp
from utils.misc import di


@dp.message_handler(Command("info"))
async def get_season_info(message: message):
    reply_msg: str = ""
    try:
        season_state: str =  f"Ближайший тур: {di.match_day}"
        season: str = f"{di.start_date[-4:]}-{di.end_date[-4:]}"
        if datetime.today() > datetime.strptime(
                                      di.end_date, '%d.%m.%Y'):
            season_state = "Турнир завершен."
        reply_msg = "\n".join(
            [
                hbold(f"{di.name} сезон {season}\n"),
                hitalic("Чемпионшип Английской футбольной лиги (официальное спонсорское название Sky Bet Чемпионшип), также известный как просто Чемпионшип (англ. Championship) — высший дивизион Английской футбольной лиги и второй по значимости дивизион в системе футбольных лиг Англии после Премьер-лиги."),
                hitalic("Чемпионшип был основан в 2004 году вместо Первого дивизиона Футбольной лиги. По данным Deloitte, в сезоне 2004/05 он был признан самым богатым вторым футбольным дивизионом в мире и шестым богатейшим дивизионом в Европе."),
                hitalic("Победители Чемпионшипа получают тот же трофей, что и выдавался победителю старого Первого дивизиона, а титул чемпиона Англии с сезона 1992/93 стал передаваться победителю Премьер-лиги.\n"),
                hbold("Период проведения:") + f" с {di.start_date} по {di.end_date}.",
                hbold(f"\n{season_state}\n"),
            ]
        )
        await message.answer(reply_msg, reply_markup=info_menu)   
    except Exception as e:
        logging.exception(f"Ошибка при формировании результата: {repr(e)}")
        await message.answer("Сервис временно недоступен", reply_markup=ReplyKeyboardRemove())
