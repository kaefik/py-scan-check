from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
import logging
import subprocess
import io
import time

from py_scan_check_fns import py_scan_check
from getinfo_check import getinfo_fns

ABOUT = range(1)

allow_users = [{"username":"Oilnur","id":"3608708"}]

path_check = "data_check/"

# проверка на разрешенного пользователя
def is_allow_user(func):
    def wrapped(*args, **kwargs):
        nameuser = args[2].message.from_user.username
        print("Имя пользователя: ", nameuser)
        for user in allow_users:
            if user["username"]==nameuser:
                return func(*args, **kwargs)
        args[2].message.reply_text(text="Доступ запрещен. Обратитесь к администратору.")
        return False
    return wrapped


class iTelegramBot:
    def __init__(self, token=None,level_loggining=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=level_loggining)
        self.bot = Updater(token)
        # обработка документов
        handlerPhoto = MessageHandler(filters = Filters.photo, callback=self.get_photo)
        self.bot.dispatcher.add_handler(handlerPhoto)
        handlerText = MessageHandler(filters = Filters.text, callback=self.get_text)
        self.bot.dispatcher.add_handler(handlerText)
        
        # регистрация обработчика для inline клавиатуры
        self.bot.dispatcher.add_handler(CallbackQueryHandler(self.inlinebutton))   
        # регистрация команд     
        self.reg_handler("start",self.start)
        self.reg_handler("about",self.about)

    # обработка получение фото от пользователя (сохранение в указанной папке)
    def get_photo(self,bot,update):
        #print("Кол-во переданных фоток: ", update.message.photo.PhotoSize)
        file_id = update.message.photo[-1].file_id
        # генерация имени фото
        filename = "1.jpg"
        newFile = bot.get_file(file_id)
        path_check_full = path_check+filename
        print("Названия фото: ", path_check_full)
        newFile.download(path_check_full)
        time.sleep(1)
        result = py_scan_check(path_check_full)
        update.message.reply_text(result.json())

    # получение текста и попытка его обработки для получения данных с серверов фнс
    def get_text(self,bot,update):
        text = update.message.text
        text_split = text.split(" ")
        if len(text_split)<3:
            update.message.reply_text("Неверные входные данные. Поробуйте снова: ФН ФД ФП")    
        else:
            result = getinfo_fns(text_split[0], text_split[1], text_split[2])
            if result.status_code != 200:
                res = "Неверные входные данные или проблема в соединении с серверами ФНС."
            else:
                res = result.json()
            update.message.reply_text(res)

    def reg_handler(self, command=None,hand=None):
        """ регистрация команд которые обрабатывает бот """
        if (command is None) or (hand is None):
            return
        self.bot.dispatcher.add_handler(CommandHandler(command, hand))
        

    def about(self, bot, update):
        """ сообщает какие есть возможности у бота """
        update.message.reply_text("Скан чека и получение информации из ФНС (проверка чека).")
    
    @is_allow_user
    def start(self, bot, update):
        update.message.reply_text('Привет {}! Отправь мне скан чека и пришлю расшифоровку чека, если чек верный.'.format(update.message.from_user.first_name))
        
    def inlinebutton(self, bot, update):
        query = update.callback_query
        
        if format(query.data)=="about":
            pass
        else:
            bot.edit_message_text(text="{}".format(query.data),
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id) 
          
    def run(self):
        """ запуск бота """   
        logging.debug("Start telegram bot")  
        self.bot.start_polling()
        self.bot.idle()

    
cfg = Config("config.ini")
tgbot = iTelegramBot(cfg.token,logging.DEBUG)
tgbot.run()