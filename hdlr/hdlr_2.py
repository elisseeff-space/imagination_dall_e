from aiogram import Router, F
from random import randint
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from config_assistants import ConfigBox
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

router = Router()

# Хэндлер на команду /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = "\n "
    help_text += ""
    help_text += "\n"
    help_text += ""
    content = as_list(
        as_marked_section(
            Bold("Иструкция по применению!"),
            as_key_value("Всего два правила использования бота", 2),
            #as_key_value("Success", 3),
            marker="  ",
        ),
        as_marked_section(
            Bold("1. командой /role можно задать инструкцию боту, чтобы он лучше понимал, что ему надо делать."),
            "Например: Инструкция: Найди все упомянутые даты и время в тексте. Выпиши их, каждый с новой строки. \n Пример результата: 22-01-2019 17:00 Завтра 18:15 Вчера Если в тексте нет дат, верни 0.\n",
            "Или: Ты — опытный копирайтер. Сгенерируй 5 опций заголовка для маркетингового текста, чтобы привлечь внимание читателей.",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("2. Если бот добавлен в группу, и нужно чтобы он проигнорировал сообщение, то есть НЕ отвечал на него, надо добавить символ @ в сообщение."),
            "Например, адресно обратиться к одному из участников.\n Тогда бот не будет мешать своими ответами.",
            marker="✅ ",
        ),
        #as_marked_section(
        #    Bold("Failed:"),
        #    "Test 2",
        #    marker="❌ ",
        #),
        
        HashTag("#OpenAI Assistant"),
        sep="\n\n",
    )
    await message.reply(**content.as_kwargs())

@router.message(Command("control"))
async def cmd_control(message: types.Message):
        #await message.answer(f"Chat {_}: {len(ConfigBox.assistant_messages[_])} items.")
    for chat_id in ConfigBox.dialog_treads.keys() :
        messages = ConfigBox.client.beta.threads.messages.list(
            thread_id=ConfigBox.dialog_treads[chat_id].id
            )
        await message.answer(f"In chat: {chat_id}, {len(messages.data)} messages.\n")

@router.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')

@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

@router.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())

@router.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )
    # или просто await callback.answer()