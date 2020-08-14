from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)

from keyboards.inline.callback_data import info_callback

info_menu = InlineKeyboardMarkup(row_width=2,
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
                                     [
                                         InlineKeyboardButton(
                                             text="История",
                                             callback_data=info_callback.new(
                                                 item="history", matchday=0)
                                         )
                                     ],

                                 ])
