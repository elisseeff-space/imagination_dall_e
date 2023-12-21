import json, os
import logging
import sqlite3 as sq
from enum import Enum
from openai import OpenAI

class imagination_Config():
    logger = logging.getLogger(__name__)
    # настройка обработчика и форматировщика для logger
    if os.name == 'posix': 
        file_name = "/home/pavel/github/imagination_dall_e/log/imagination.log"
    elif os.name == 'nt':
        file_name = r'C:\Users\Eliseev\GitHub\imagination_dall_e\log\imagination.log'
    else: raise ValueError("Unsupported operating system")

    handler = logging.FileHandler(file_name, mode='w')
    #formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %I:%M:%S')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %H:%M:%S')

    client: OpenAI
    assistant: OpenAI
    
    dialog_messages = {}

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
        if os.name == 'posix': filename = "/home/pavel/github/imagination_dall_e/db/imagination_dall_e.db"
        elif os.name == 'nt': filename = str(r'C:\Users\Eliseev\GitHub\imagination_dall_e\db\imagination_dall_e.db')
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

    @classmethod
    
    @classmethod
    def set_logger_name(self, logger_name: str)->bool:
        self.logger.name = logger_name
    
    @classmethod
    def update_dialog(self, chat_id: str, dialog_message: str)->bool:
        if chat_id in self.dialog_messages.keys() : self.dialog_messages[chat_id].append(dialog_message)
        else : self.dialog_messages[chat_id] = []

ConfigBox = imagination_Config()

if __name__ == '__main__':
    print("Hello!")
    
    ConfigBox.logger.warning('New elis_openai_ii_Config successfully init!')