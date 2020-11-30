from telepot.namedtuple import KeyboardButton,ReplyKeyboardMarkup
import telepot as t
from flask import Flask, request
import time
import urllib3

proxy_url = "http://proxy.server:3128"
t.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
t.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts



token='<YOUR TELEGRAM API TOKEN>'
secret= '<ANY ALPHA_NUMERIC STRING'

start=0
answer_list=[0]
question_list=['','60+5','2+1+2-1','41*3','80*100','20100/300','123*534','875*10','5*5','1+1','90-423']
option_list=['',
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='56'),KeyboardButton(text='605')],[KeyboardButton(text='65'),KeyboardButton(text='506')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='42'),KeyboardButton(text='0')],[KeyboardButton(text='22'),KeyboardButton(text='4')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='123'),KeyboardButton(text='341')],[KeyboardButton(text='433'),KeyboardButton(text='742')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='8100'),KeyboardButton(text='180')],[KeyboardButton(text='80000'),KeyboardButton(text='8000')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='67'),KeyboardButton(text='200300')],[KeyboardButton(text='2300'),KeyboardButton(text='6050')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='54321'),KeyboardButton(text='534123')],[KeyboardButton(text='123534'),KeyboardButton(text='65682')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='5520'),KeyboardButton(text='63720')],[KeyboardButton(text='8750'),KeyboardButton(text='62560')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='10'),KeyboardButton(text='225')],[KeyboardButton(text='25'),KeyboardButton(text='0')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='01'),KeyboardButton(text='2')],[KeyboardButton(text='11'),KeyboardButton(text='1')]]),
      ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='-43'),KeyboardButton(text='-343')],[KeyboardButton(text='333'),KeyboardButton(text='-333')]])
      ]
correct_answer_list=[0,65,4,123,8000,67,65682,8750,25,2,-333]

bot=t.Bot(token)



bot.deleteWebhook()

bot.setWebhook("https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"

# DRIVER LOOP...
def main(ms):
    global answer_list
    global start
    i=ms['chat']['id']
    tsg=ms['text']
    try:
    	print(ms['from']['username'],' : ',tsg)
    except:
    	print(tsg)
    print('\n')

    if tsg=='/start':
        try:
        	bot.sendMessage(i,'Hi! '+ms['from']['username']+' !!!'+' \n\nI am created by ~TSG~, Wanna have a Quick Math test ? \n\n~From DARK',reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start Test'),KeyboardButton(text='No Thanks!')]]))
        except:
        	bot.sendMessage(i,'Hi!  \n\nI am created by ~TSG~, Wanna have a Quick Math test ? \n\n~From DARK',reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start Test'),KeyboardButton(text='No Thanks!')]]))
    if tsg=='Start Test' or tsg=='Try Again':
        start=1
    if tsg=='No Thanks!':
        bot.sendMessage(i,"Ok no problem!! To start the Test, type or click on ---> /start \n\nMeanwhile you can check my creator's Github A/c and Follow it!! \n\n~Thank You,\n      DARK",reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Visit Github!')]]))
    if tsg=='Visit Github!':
        bot.sendMessage(i,"https://github.com/TSG405",reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start Test')]]))
    if start and start<12:
        if tsg!='Start Test' and tsg!='Try Again' and tsg!='No Thanks!'and tsg!='Visit Github!':
            answer_list.append(int(tsg))
        if start<11:
            bot.sendMessage(i,"What is --> "+question_list[start]+" ??",reply_markup=option_list[start])
        else:
            start=co=0
            no=-1
            print("USER ENTERED:",answer_list)
            for i in answer_list:
                if i==correct_answer_list[co]:
                    no=no+1
                co=co+1
            answer_list=[0]
            bot.sendMessage(ms['chat']['id'],'\nHey! You just finished your test!! Let me get you the score!\nSo, the number of right answers :-- '+str(no)+' out of 10 !',reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Wanna Try Again??'),KeyboardButton(text='No Thanks!')]]))
        if start!=0:
            start+=1

bot.message_loop(main)
while 1:
    time.sleep(10)

'''@CODED BY TSG,2020'''
