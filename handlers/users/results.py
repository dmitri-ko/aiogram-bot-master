import logging

from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from utils.misc.matchday import MatchDay
from keyboards.inline.matchday_buttons import matchday_menu, matchdays
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hitalic
from loader import dp
from aiogram.dispatcher.filters.builtin import Command
from keyboards.inline import info_callback
from utils.misc import di


@dp.callback_query_handler(info_callback.filter(item="results"))
async def cb_send_matchdays(call: CallbackQuery) -> None:
    await call.answer(cache_time=60)
    reply_msg: str = "Выберите тур:"
    await call.message.answer(reply_msg, reply_markup=matchdays)


@dp.message_handler(Command("results"))
async def send_matchdays(message: Message) -> None:
    await message.answer("Выберите тур:", reply_markup=matchdays)


@dp.callback_query_handler(info_callback.filter(item="matchday"))
async def send_matchday_results(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    try:
        matchday: int = int(callback_data.get("matchday"))
        reply_msg: str = f"<b>Тур {matchday}. Результаты матчей:</b>\n\n"
        matches: MatchDay = di.get_matches(matchday)
        for match in matches.games:
            reply_msg += hitalic(f"{match.home_team} - {match.away_team}") + \
                " " + hbold(f"{match.home_goals}:{match.away_goals}") + "\n"
        await call.message.answer(text=reply_msg, reply_markup=matchday_menu)
    except (AttributeError, KeyError, IndexError) as e:
        logging.exception(e)
        await call.message.answer(text="За выбранный период результатов игр нет", reply_markup=ReplyKeyboardRemove())
