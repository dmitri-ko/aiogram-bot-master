import logging
import re
from datetime import datetime
from typing import AnyStr, Dict, List, Pattern, Union

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from data.config import ROW_SIZE
from keyboards.inline import info_callback
from keyboards.inline.fixtures_buttons import fixtures_buttons
from keyboards.inline.matchday_buttons import matchday_menu
from loader import dp
from utils.misc import di
from utils.misc.data_interface import EFLData, MatchStatus
from utils.misc.matchday import Fixtures, MatchDay


@dp.message_handler(Command("results"))
async def send_matchdays(message: Message) -> None:
    pattern: Pattern[AnyStr] = re.compile(r"^[0-9]+$")
    fixtures: Fixtures = di.get_fixtures(status=MatchStatus.FINISHED)
    if fixtures:
        last_round_num = list(fixtures.matchdays)[-1]
        last_round = fixtures.matchdays.get(last_round_num)
        reply_msg: str = hbold(
            f"Результаты игр {EFLData.get_matchday_desc(matchday_id=last_round_num,prefix=True)}:\n")
        match_date: datetime = datetime.today()
        for match in last_round.games:
            if match.date.strftime("%Y-%m-%d") != match_date.strftime("%Y-%m-%d"):
                match_date = match.date
                reply_msg += hbold(f"\n{match.date.strftime('%d.%m.%Y')}\n")
            reply_msg += match.scores
        await message.answer(text=reply_msg, reply_markup=ReplyKeyboardRemove())

        allButtons: List[InlineKeyboardButton] = [
            InlineKeyboardButton(text=f"{matchday}", callback_data=info_callback.new(item="matchday", matchday=matchday)) for matchday in fixtures.matchdays.keys() if matchday != last_round_num and pattern.match(matchday)
        ]
        if len(allButtons) != 0:
            fixtures_buttons.inline_keyboard.clear()
            for i in range(0, len(allButtons)//ROW_SIZE+1):
                fixtures_buttons.row(
                    *allButtons[i*ROW_SIZE:i*ROW_SIZE+ROW_SIZE])
            reply_msg = hbold("Регулярный сезон:")
            await message.answer(text=reply_msg, reply_markup=fixtures_buttons)

        allButtons.clear()
        allButtons = [
            InlineKeyboardButton(text=f"{EFLData.get_matchday_desc(matchday)}", callback_data=info_callback.new(item="matchday", matchday=matchday)) for matchday in fixtures.matchdays.keys() if matchday != last_round_num and not pattern.match(matchday)
        ]
        if len(allButtons) != 0:
            fixtures_buttons.inline_keyboard.clear()
            for i in range(0, len(allButtons)//ROW_SIZE+1):
                fixtures_buttons.row(
                    *allButtons[i*ROW_SIZE:i*ROW_SIZE+ROW_SIZE])
            reply_msg = hbold("Плейофф:")
            await message.answer(text=reply_msg, reply_markup=fixtures_buttons)
    else:
        await message.answer(text="Игр нет.")


@dp.callback_query_handler(info_callback.filter(item="results"))
async def cb_send_matchdays(call: CallbackQuery) -> None:
    await call.answer(cache_time=60)
    await send_matchdays(message=call.message)


@dp.callback_query_handler(info_callback.filter(item="matchday"))
async def send_matchday_results(call: CallbackQuery, callback_data: dict) -> None:
    filter: Dict[str, Union[str, int]] = {}
    await call.answer(cache_time=60)
    try:
        matchday_id: str = str(callback_data.get("matchday"))
        reply_msg: str = hbold(
            f"Результаты матчей {EFLData.get_matchday_desc(matchday_id=matchday_id,prefix=True)}:\n")
        if matchday_id.isdigit():
            filter["matchday"] = int(matchday_id)
        else:
            filter["stage"] = matchday_id
        
        matches: MatchDay = di.get_matches(**filter)
        match_date: datetime = datetime.today()
        for match in matches.games:
            if match.date.strftime("%Y-%m-%d") != match_date.strftime("%Y-%m-%d"):
                match_date = match.date
                reply_msg += hbold(f"\n{match.date.strftime('%d.%m.%Y')}\n")
            reply_msg += match.scores
        await call.message.answer(text=reply_msg, reply_markup=matchday_menu)
    except (AttributeError, KeyError, IndexError) as e:
        logging.exception(e)
        await call.message.answer(text="За выбранный период результатов игр нет", reply_markup=ReplyKeyboardRemove())
