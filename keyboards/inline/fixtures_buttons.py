from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)

from data.config import ROW_SIZE
from keyboards.inline.callback_data import info_callback
from utils.misc import di

fixtures_buttons = InlineKeyboardMarkup(row_width=ROW_SIZE)                                 
