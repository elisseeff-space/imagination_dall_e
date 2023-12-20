from datetime import datetime
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from config_assistants import ConfigBox
from assistants_request import assistant_run
#from openai import AsyncOpenAI

open_ai_role_dict = {}

router = Router()

# Хэндлер на команду /test1
@router.message(Command("role"))
async def set_assistant_instructions(
            message: Message,
            command: CommandObject
    ):
    #ya_gpt_role = message.text
    #await message.reply(f"role set ok! {ya_gpt_role}")
    
    #global open_ai_role_dict

    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        #open_ai_role_dict[str(message.chat.id)] = command.args
        ConfigBox.set_dialog_instructions(str(message.chat.id), command.args)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/role <Описание роли>"
        )
        return
    await message.answer(
        "Роль установлена!\n"
        f"Текст: {command.args}"
    )

@router.message(F.text)
async def message_with_text(message: Message):
    
    #query = message.text.replace('"', '^')
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    if flag is False :
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        if chat_id in ConfigBox.dialog_treads.keys() :
            ConfigBox.update_dialog(chat_id, "user", query)
        else:
            ConfigBox.create_dialog(chat_id, query)
        
        assistant__response = await assistant_run(chat_id, message)
        
        use_date = str(datetime.now())
        #time_now = datetime.now().strftime('%H:%M')
        if len(assistant__response) > 0 :
            for _ in assistant__response :
                _ = _.replace('"', '^')
                params = (chat_id, user_id, use_date, ConfigBox.dialog_instructions[chat_id], query, _, 0, 0, 0)
                ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
                ConfigBox.dbase.commit()

                #ConfigBox.update_dialog(chat_id, "assistant", _)
                await message.answer(f"{_}")
        else : 
            await message.answer("Ответ не получен. Наверное что-то случилось")
    else : 
        await message.answer("Я молчу...")
    
@router.edited_message(F.text)
async def edited_message_with_text(message: Message):
    
    await message.answer("Message is edited...")