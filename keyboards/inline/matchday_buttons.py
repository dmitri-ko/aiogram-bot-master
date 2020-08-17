from keyboards.inline.callback_data import info_callback
from utils.misc import di
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

ROW_SIZE: int = 6
rows: int = di.match_day//ROW_SIZE+1

matchdays = InlineKeyboardMarkup(row_width=ROW_SIZE,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text=f"{matchday}", callback_data=info_callback.new(item="matchday", matchday=matchday)) for matchday in range(row*ROW_SIZE+1, min(row*ROW_SIZE+1 + ROW_SIZE, di.match_day+1))
                                     ] for row in range(0, rows)
                                 ]
                                 )

matchday_menu = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(
                                                 text="Турнирная таблица",
                                                 callback_data=info_callback.new(item="standings", matchday=0))
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Результаты",
                                                 callback_data=info_callback.new(item="results", matchday=0)),
                                             InlineKeyboardButton(
                                                 text="Расписание",
                                                 callback_data=info_callback.new(
                                                     item="fixtures", matchday=0)
                                             )
                                         ],
                                     ])
