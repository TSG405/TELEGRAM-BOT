'''
Online script hosting via Flask,requests,Telegram-API.
PythonAnywhere account is utilized.
'''

import telebot
from flask import Flask, request

token ='<TOKEN>'
secret = '<RANDOM ALPHA_NUMERIC STRING>'

bot=telebot.TeleBot(token,threaded=False)

bot.remove_webhook()
bot.set_webhook(url=('https://USERNAME.pythonanywhere.com/'+secret))

app=Flask(__name__)
@app.route('/'+secret, methods=['POST'])
def webhook():
    update=telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'Ok',200

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,'Hello, User!! How may I help you, today??')

@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id,'Hello, please help yourself!')
    
@bot.message_handler(commands=['tsg'])
def tsg(m):
    bot.send_message(m.chat.id,'Hello, CREATOR!!! I am at your commands.... @TSG')
