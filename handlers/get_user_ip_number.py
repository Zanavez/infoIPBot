import asyncio
import datetime
import re
import asyncpg
import requests
from aiogram import types, Router, F
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiohttp import ClientSession
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

get_user_ip_number_router = Router()
pattern = r'^\d{5}/\d{2}/\d{5}-ИП$'


@get_user_ip_number_router.message()
async def message_handler(message: types.Message):
    if re.match(pattern, message.text):
        async with ClientSession() as session:
            async with session.get(
                    f"https://portal9.ru/fssp/8f9a3c8a5fb6b734a00295cd6cc12705/iplegallist?ep_number={message.text}"
            ) as response:
                response = await response.json()
                values = list(response['data'][0].values())

                print(response)
                print(values, len(values))

                builder = InlineKeyboardBuilder()
                builder.row(types.InlineKeyboardButton(
                    text="Обновить", callback_data=f"update:{values[4]}+{message.message_id}")
                )

                await message.reply(
                    f"<b>Номер ИП: <code>{values[4] if values[4] is not None else 'н/д'}</code></b>\n"
                    f"<b>Номер сводного ИП: <code>{values[6] if values[6] is not None else 'н/д'}</code></b>\n"
                    f"<b>Должник: <code>{values[1] if values[1] is not None else 'н/д'}</code></b>\n"
                    f"<b>Адрес: <code>{values[2] if values[2] is not None else 'н/д'}</code></b>\n"
                    f"<b>Фактический адрес: <code>{values[3] if values[3] is not None else 'н/д'}</code></b>\n"
                    f"<b>Дата возбуждения: <code>{datetime.datetime.strptime(values[5], '%Y-%m-%d').strftime('%d.%m.%Y') if values[5] is not None else 'н/д'}</code></b>\n"
                    f"<b>Тип исполнительного документа: <code>{values[7] if values[7] is not None else 'н/д'}</code></b>\n"
                    f"<b>Дата исполнительного документа: <code>{datetime.datetime.strptime(values[8], '%Y-%m-%d').strftime('%d.%m.%Y') if values[8] is not None else 'н/д'}</code></b>\n"
                    f"<b>Номер исполнительного документа: <code>{values[9] if values[9] is not None else 'н/д'}</code></b>\n"
                    f"<b>Требования исполнительного документа: <code>{values[10] if values[10] is not None else 'н/д'}</code></b>\n"
                    f"<b>Предмет исполнения: <code>{values[11] if values[11] is not None else 'н/д'}</code></b>\n"
                    f"<b>Сумма к оплате: <code>{values[12] if values[12] is not None else 'н/д'} руб.</code></b>\n"
                    f"<b>Остаток долга: <code>{values[13] if values[13] is not None else 'н/д'} руб.</code></b>\n"
                    f"<b>Отдел судебных приставов: <code>{values[14] if values[14] is not None else 'н/д'}</code></b>\n"
                    f"<b>Адрес отдела судебных приставов: <code>{values[15] if values[15] is not None else 'н/д'}</code></b>\n"
                    f"<b>ИНН должника: <code>{values[16] if values[16] is not None else 'н/д'}</code></b>\n"
                    f"<b>ИНН взыскателя-организации: <code>{values[17] if values[17] is not None else 'н/д'}</code></b>\n"
                    f"<b>Последняя проверка: <code>{datetime.datetime.fromtimestamp(values[19]).strftime('%d.%m.%Y, %H:%M:%S') if values[19] is not None else 'н/д'}</code></b>\n"
                    f"<b>Последнее изменение: <code>{datetime.datetime.fromtimestamp(values[20]).strftime('%d.%m.%Y, %H:%M:%S') if values[20] is not None else 'н/д'}</code></b>\n",
                    disable_web_page_preview=True, parse_mode=ParseMode.HTML, reply_markup=builder.as_markup()
                )
    else:
        await message.reply("<b>Неправильно введены данные, введите их в формате <code>XXXXX/YY/ZZZZZ-ИП</code></b>", disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@get_user_ip_number_router.callback_query(lambda c: c.data.startswith('update'))
async def update_ip_status(callback: types.CallbackQuery):
    print(callback.data)
    clb_data = callback.data.split(':')[1]
    ep_number = clb_data.split('+')[0]
    msg_id = clb_data.split('+')[1]

    async with ClientSession() as session:
        async with session.get(
                f"https://portal9.ru/fssp/8f9a3c8a5fb6b734a00295cd6cc12705/iplegallist?ep_number={ep_number}") as response:
            response = await response.json()
            print(response)
            values = list(response['data'][0].values())


    new_text = (f"Never Gonna Give You Up: {values[4] if values[4] is not None else 'н/д'}\n"
                f"Never Gonna Let You Down: {values[6] if values[6] is not None else 'н/д'}\n"
                f"Never Gonna Round Around And Desert You: {values[1] if values[1] is not None else 'н/д'}\n"
                f"Never Gonna Make You Cry: {values[2] if values[2] is not None else 'н/д'}\n"
                f"Never Gonna Say Goodbye: {values[3] if values[3] is not None else 'н/д'}\n"
                f"Never Gonna Tell A Lie and Hurt you: {datetime.datetime.strptime(values[5], '%Y-%m-%d').strftime('%d.%m.%Y') if values[5] is not None else 'н/д'}\n"
                f"Тип исполнительного документа: {values[7] if values[7] is not None else 'н/д'}\n"
                f"Дата исполнительного документа: {datetime.datetime.strptime(values[8], '%Y-%m-%d').strftime('%d.%m.%Y') if values[8] is not None else 'н/д'}\n"
                f"Номер исполнительного документа: {values[9] if values[9] is not None else 'н/д'}\n"
                f"Требования исполнительного документа: {values[10] if values[10] is not None else 'н/д'}\n"
                f"Предмет исполнения: {values[11] if values[11] is not None else 'н/д'}\n"
                f"Сумма к оплате: {values[12] if values[12] is not None else 'н/д'} руб.\n"
                f"Остаток долга: {values[13] if values[13] is not None else 'н/д'} руб.\n"
                f"Отдел судебных приставов: {values[14] if values[14] is not None else 'н/д'}\n"
                f"Адрес отдела судебных приставов: {values[15] if values[15] is not None else 'н/д'}\n"
                f"ИНН должника: {values[16] if values[16] is not None else 'н/д'}\n"
                f"ИНН взыскателя-организации: {values[17] if values[17] is not None else 'н/д'}\n"
                f"Последняя проверка: {datetime.datetime.fromtimestamp(values[19]).strftime('%d.%m.%Y, %H:%M:%S') if values[19] is not None else 'н/д'}\n"
                f"Последнее изменение: {datetime.datetime.fromtimestamp(values[20]).strftime('%d.%m.%Y, %H:%M:%S') if values[20] is not None else 'н/д'}\n")
    await asyncio.sleep(1)
    await callback.message.edit_text(message_id=int(msg_id), text=new_text)
