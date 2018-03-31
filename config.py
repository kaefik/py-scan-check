""" Хранение настроек приложения """

import os
import csv
import configparser

class Config:
    
    def __init__(self,namefile_cfg = "config.ini"):
        self.namefile_cfg = namefile_cfg
        self.username=None
        self.code=None
        if not os.path.exists(self.namefile_cfg):
            raise FileExistsError("Не найден файл конфигурации {}.\nСоздайте config.ini из файла config.ini.sample.".format(namefile_cfg))
        config = configparser.ConfigParser()
        config.read(self.namefile_cfg)
        self.username = str(config['AUTORIZATION']['username'])
        self.code = str(config['AUTORIZATION']['code'])
        self.token = str(config['BOT']['token'])