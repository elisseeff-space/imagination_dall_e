import json, os
import logging
import sqlite3 as sq
from enum import Enum
from openai import OpenAI

class imagination_Config():
    logger = logging.getLogger(__name__)
    # настройка обработчика и форматировщика для logger
    if os.name == 'posix': 
        file_name = "/home/pavel/github/assistants_openai/log/assistants_openai.log"
    elif os.name == 'nt':
        file_name = r'C:\Users\Eliseev\GitHub\assistants_openai\log\assistants_openai.log'
    else: raise ValueError("Unsupported operating system")

    handler = logging.FileHandler(file_name, mode='w')
    #formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %I:%M:%S')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %H:%M:%S')

    client: OpenAI
    assistant: OpenAI
    dialog_instructions = {}
    dialog_treads = {}
    dialog_messages_of_assistant = []

    #open_ai_prefix = {}

    @classmethod
    def __init__(self):
        
        # Set up logger
        # self.logging #.info('Verify successfully init!')
        
        self.logger.setLevel(logging.INFO)
        
        # добавление форматировщика к обработчику
        self.handler.setFormatter(self.formatter)
        # добавление обработчика к логгеру
        self.logger.addHandler(self.handler)

        #self.StepQuantity = 878
        if os.name == 'posix': filename = "/home/pavel/github/assistants_openai/db/assistants_openai.db"
        elif os.name == 'nt': filename = str(r'C:\Users\Eliseev\GitHub\assistants_openai\db\assistants_openai.db')
        else: raise ValueError("Unsupported operating system")
        self.dbase = sq.connect(filename)
        self.cur = self.dbase.cursor()
        

        if os.name == 'posix': in_file = "/home/pavel/cfg/config.json"
        elif os.name == 'nt': in_file = str(r'C:\Users\Eliseev\GitHub\cfg\config.json')
        else: raise ValueError("Unsupported operating system")
        file = open(in_file, 'r')
        self.config = json.load(file)

        # create OpenAI connection

        self.client = OpenAI(api_key = self.config['openai'])

        self.assistant = self.client.beta.assistants.create(
            name="Python Programmer",
            description="My first Assistant Elis",
            instructions="You are a personal developyng tutor. Write and run code to develop Python application for using with Telegram messendger and aiogram library.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )

        self.dialog_instructions['First Test'] = "Ты профессионал программист."

    @classmethod
    def message_not_exists(self, message_id: str)->bool:
        flag_if_exists = False
        if message_id in self.dialog_messages_of_assistant : flag_if_exists = False
        else : 
            self.dialog_messages_of_assistant.append(message_id)
            flag_if_exists = True
        return flag_if_exists
    
    @classmethod
    def set_logger_name(self, logger_name: str)->bool:
        self.logger.name = logger_name
    
    @classmethod
    def create_dialog(self, chat_id: str, query: str)->bool:
        self.logger.name = 'elis_openai_ii_Config.create_dialog'

        #self.assistant_messages[chat_id] = [{
        #    "role": role,
        #    "content": message
        #}]

        self.dialog_treads[chat_id] = self.client.beta.threads.create(messages= [])
        message = self.client.beta.threads.messages.create(
            thread_id=self.dialog_treads[chat_id].id,
            role="user",
            content=query
        )
        self.dialog_instructions[chat_id] = "Ты профессионал программист"

        return True
    
    @classmethod
    def set_dialog_instructions(self, chat_id: str, role: str)->bool:
        self.dialog_instructions[chat_id] = role

    @classmethod
    def update_dialog(self, chat_id: str, role_1: str, query: str)->bool:
        
        message = self.client.beta.threads.messages.create(
            thread_id=self.dialog_treads[chat_id].id,
            role=role_1,
            content=query
        )

ConfigBox = imagination_Config()

if __name__ == '__main__':
    print("Hello!")
    
    ConfigBox.logger.warning('New elis_openai_ii_Config successfully init!')