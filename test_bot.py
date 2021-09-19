import time
import os
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('tg_token')  # добавить токен тг
token_vk = os.getenv('token_vk')

STATE=None
# function to handle the /start command
def start(update, context):
    update.message.reply_text('Получена команда start')
# function to handle the /help command
def help(update, context):
    update.message.reply_text('Получена команда help')
# function to handle errors occured in the dispatcher 
def error(update, context):
    update.message.reply_text('Произошла ошибка')
# function to handle normal text 
def text(update, context):
    if STATE == 'vk':
        id = update.message.text
        context.user_data['vk_id'] = id
        get_status(update, context)
    else:
        text_received = update.message.text
        update.message.reply_text(f'Ты сказал "{text_received}" ?')

def status(update, context):
    global STATE
    STATE = 'vk'
    update.message.reply_text('Введите Id')

def get_status(update, context): 
    params = {
        'access_token': token_vk,
        'v': '5.92',
        'fields': 'online',
        'user_id': context.user_data['vk_id'] 
    }
    result = requests.post('https://api.vk.com/method/users.get', data = params).json()['response']
    result_status = (result[0]['online']) #проверка пользователя online
    print(result_status)
    if result_status == 1:
        update.message.reply_text('Онлайн')
    else:
        update.message.reply_text('Офлайн')


def main():
    TOKEN = os.getenv('tg_token')
    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    # add an handler for errors
    dispatcher.add_error_handler(error)
    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()