import asyncio
import logging

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ChatActions, Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from keyboards.inline.callback_data import info_callback
from keyboards.inline.standings_button import standings_menu
from loader import bot, dp
from utils.misc import di
from utils.misc.file_cache import TelegramFileCache
from utils.misc.html_2_image import StandingsRenderer
from utils.misc.standings_data import Standings


@dp.message_handler(Command("standings"))
async def send_standings(message: Message) -> None:

    row_template = """<tr>
                           <td class='ph-0 w-20' {}>{}</td>
                           <td class='team pl-10'>{}</td>
                           <td >{}</td>
                           <td>{}</td>
                           <td>{}</td>
                           <td>{}</td>
                           <td>{}-{}</td>
                           <td class='p-0 ta-right'>{}</td>
                        </tr>
                    """

    try:
        standings: Standings = di.get_standings()
        table_img_filename: str = (
            "data/images/standings-" + standings.last_updated + ".jpg"
        )

        media_library = TelegramFileCache()
        file_id: str = media_library.get_id(table_img_filename)
        if file_id == None:
            #config = imgkit.config(wkhtmltoimage="/app/bin/wkhtmltoimage")
            msg_body: str = ""

            for position in standings.table:
                if position.zone == "promotion":
                    col_style = "style='background-color: #138B43;'"
                elif position.zone == "playoff":
                    col_style = "style='background-color: #00B900;'"
                elif position.zone == "relegation":
                    col_style = "style='background-color: #F05632;'"
                else:
                    col_style = ""
                msg_body += row_template.format(
                    col_style,
                    position.position,
                    position.team,
                    position.games,
                    position.won,
                    position.draw,
                    position.lost,
                    position.goals_for,
                    position.goals_against,
                    position.points,
                )

            

            await asyncio.sleep(1)
            await bot.send_chat_action(message.from_user.id, ChatActions.UPLOAD_PHOTO)

            renderer: StandingsRenderer = StandingsRenderer()
            renderer.make_img(template_body=msg_body, path_to_img=table_img_filename)
            
            file_id = await media_library.generate_id(
                table_img_filename, message.chat.id
            )
            if file_id == None:
                raise Exception(f"Invalid file id {file_id}")
        
        reply_msg: str = "<b>EFL. Турнирная таблица:</b>  \n\n"    
        await message.answer(reply_msg)
        await message.answer_photo(photo=file_id, reply_markup=standings_menu)

    except Exception as err:
        logging.exception(err)
        await message.answer(text="Сервис временно недоступен", reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(info_callback.filter(item="standings"))
async def cb_send_standings(call: CallbackQuery):
    await call.answer(cache_time=60)
    await send_standings(call.message)
