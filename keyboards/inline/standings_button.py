from keyboards.inline.callback_data import info_callback
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

standings_menu = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
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
