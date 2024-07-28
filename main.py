import telebot
from extensions import APIException, CurrencyConverter
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = "Чтобы узнать курс валюты, отправьте сообщение в формате:\n<имя валюты цену которой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in CurrencyConverter.keys:
        text += f'\n{i}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
       values = message.text.split()
       if len(values) != 3:
           raise APIException('Неверное количество параметров')

       base, quote, amount = values
       result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {result}'
        bot.reply_to(message, text)
bot.polling()