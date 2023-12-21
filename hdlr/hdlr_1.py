from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from config_imagination import ConfigBox
#from assistants_request import assistant_run
#from openai import AsyncOpenAI

router = Router()

# Хэндлер на команду /test1
@router.message(Command("role"))
async def set_assistant_instructions(
            message: Message,
            command: CommandObject
    ):

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
async def message_with_text(message: Message, bot: Bot):
    
    #query = message.text.replace('"', '^')
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    if flag is False :

        response = ConfigBox.client.images.generate(
        model="dall-e-3",
        prompt=message.text,
        size="1024x1024",
        quality="standard",
        n=1,
        )

        image_url = response.data[0].url
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        use_date = str(datetime.now())

        ConfigBox.update_dialog(chat_id, message.text)
        params = (chat_id, user_id, use_date, "imagination", message.text, _, 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        await message.answer(f"Картинка сгенерирована: {image_url}")
    else : 
        await message.answer("Я молчу...")
    
@router.edited_message(F.text)
async def edited_message_with_text(message: Message):
    
    await message.answer("Message is edited...")