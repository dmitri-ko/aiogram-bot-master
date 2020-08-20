import logging
import re
from datetime import datetime
from typing import AnyStr, Dict, List, Pattern, Union
from utils.misc.data_interface import EFLData, MatchStatus

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from data.config import ROW_SIZE
from keyboards.inline.callback_data import info_callback
from keyboards.inline.fixtures_buttons import fixtures_buttons
from keyboards.inline.matchday_buttons import matchday_menu
from loader import dp
from utils.misc import di
from utils.misc.matchday import Fixtures, MatchDay


@dp.message_handler(Command("fixtures"))
async def send_fixtures(message: Message):
    fixtures: Fixtures = di.get_fixtures()
    if fixtures:
        next_round_num, next_round = next(iter(fixtures.matchdays.items()))
        reply_msg: str = hbold(f"Расписание игр {EFLData.get_matchday_desc(matchday_id=next_round_num, prefix=True)}:\n")
        match_date: datetime = datetime.today()
        for match in next_round.games:
            if match.date.strftime("%Y-%m-%d") != match_date.strftime("%Y-%m-%d"):
                match_date = match.date
                reply_msg += hbold(f"\n{match.date.strftime('%d.%m.%Y')}\n")
            reply_msg += match.schedule
        await message.answer(text=reply_msg, reply_markup=ReplyKeyboardRemove())

        pattern: Pattern[AnyStr] = re.compile(r"^[0-9]+$")
        allButtons: List[InlineKeyboardButton] = [
            InlineKeyboardButton(text=f"{matchday}", callback_data=info_callback.new(item="fixtures", matchday=matchday)) for matchday in fixtures.matchdays.keys() if matchday != next_round_num and pattern.match(matchday)
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
            InlineKeyboardButton(text=f"{EFLData.get_matchday_desc(matchday)}", callback_data=info_callback.new(item="fixtures", matchday=matchday)) for matchday in fixtures.matchdays.keys() if matchday != next_round_num and not pattern.match(matchday)
        ]
        if len(allButtons) != 0:
            fixtures_buttons.inline_keyboard.clear()
            for i in range(0, len(allButtons)//ROW_SIZE+1):
                fixtures_buttons.row(
                    *allButtons[i*ROW_SIZE:i*ROW_SIZE+ROW_SIZE])
            reply_msg = hbold("Плейофф:")
            await message.answer(text=reply_msg, reply_markup=fixtures_buttons)
    else:
        await message.answer(text="Запланированных игр нет.")


@dp.callback_query_handler(info_callback.filter(item="fixtures"))
async def send_matchday_fixture(call: CallbackQuery, callback_data: Dict):
    reply_msg: str = ""
    filter: Dict[str,Union[str, int]] = {"status": MatchStatus.SCHEDULED}
    await call.answer(cache_time=60)
    try:
        matchday_id: str = str(callback_data.get("matchday"))
        if matchday_id != "0":
            reply_msg = hbold(f"Расписание игр {EFLData.get_matchday_desc(matchday_id=matchday_id, prefix=True)}:\n")
            if matchday_id.isdigit():
                filter["matchday"] = int(matchday_id)
            else:
                filter["stage"] = matchday_id
            
            matchday: MatchDay = di.get_matches(**filter)
            match_date: datetime = datetime.today()
            for match in matchday.games:
                if match.date.strftime("%Y-%m-%d") != match_date.strftime("%Y-%m-%d"):
                    match_date = match.date
                    reply_msg += hbold(f"\n{match.date.strftime('%d.%m.%Y')}\n")
                reply_msg += match.schedule
            await call.message.answer(text=reply_msg, reply_markup=matchday_menu)
        else:
            await send_fixtures(call.message)
    except Exception as err:
        logging.exception(err)
