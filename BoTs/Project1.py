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


token='<TELEGRAM_API_TOKEN>'
secret='<RANDOM ALPHA-NUMERIC STRING>'

start=0
mean=14
SD=6
PSC1=[0]
PSC2=['','1) In the last month, how often have you been upset because of something, that happened unexpectedly?','2) In the last month, how often have you felt that you were unable to control the important things in your life?',
      '3) In the last month, how often have you felt nervous and "stressed" ?','4) In the last month, how often have you felt confident about your ability, to handle your personal problems?',
      '5) In the last month, how often have you felt that things were going your way?','6) In the last month, how often have you found that you could not cope with all the things, that you had to do?',
      '7) In the last month, how often have you been able to control irritations in your life?','8) In the last month, how often have you felt that you were on top of things?',
      '9) In the last month, how often have you been angered because of things that were outside of your control?','10) In the last month, how often have you felt difficulties were piling up so high, that you could not overcome them?']
PSC3=['',ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0 = NEVER'),KeyboardButton(text='1 = ALMOST NEVER')],[KeyboardButton(text='2 = SOMETIMES'),KeyboardButton(text='3 = FAIRLY OFTEN')],[KeyboardButton(text='4 = VERY OFTEN')]])]

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

# DRIVER CODE...
def main(ms):
    global PSC1
    global start
    global mean
    global SD

    r1=mean+SD
    r2=mean-SD
    mid=(r1+r2)/2
    d=2

    i=ms['chat']['id']
    tsg=ms['text']
    
    try:
    	print(ms['from']['username'],' : ',tsg)
    except:
    	print(tsg)
    print('\n')

    if tsg=='/start':
        try:
        	bot.sendMessage(i,'Hi! '+ms['from']['username']+' \n\nI am created by ~TSG~, Wanna have a Quick Perceived Stress Test (designed by Sheldon Cohen) ? \n\n~ From DARK',reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start P.S Test'),KeyboardButton(text='No Thanks!')]]))
        except:
        	bot.sendMessage(i,'Hi!  \n\nI am created by ~TSG~, Wanna have a Quick Perceived Stress Test (designed by Sheldon Cohen) ? \n\n~ From DARK',reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start P.S Test'),KeyboardButton(text='No Thanks!')]]))
    if tsg=='Start P.S Test' or tsg=='Try Again':
        start=1
    if tsg=='No Thanks!':
        bot.sendMessage(i,"Ok no problem!! To start the Test, type or click on ---> /start \n\nMeanwhile you can check my creator's Github A/c and Follow it!! \n\n~Thank You,\n      DARK",reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Visit Github!')]]))
    if tsg=='Visit Github!':
        bot.sendMessage(i,"https://github.com/TSG405",reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start P.S Test')]]))
    if start and start<12:
        if tsg!='Try Again' and tsg!='No Thanks!'and tsg!='Visit Github!' and tsg!='Start P.S Test':
            PSC1.append(tsg)
        if start<11:
            bot.sendMessage(i,PSC2[start],reply_markup=PSC3[1])
        else:
            start=total=0
            pp="0"
            print("USER ENTERED:",PSC1)
            for gg in PSC1:
                if gg=='0 = NEVER':
                    total+=0
                elif gg=='1 = ALMOST NEVER':
                    total+=1
                elif gg=='2 = SOMETIMES':
                    total+=2
                elif gg=='3 = FAIRLY OFTEN':
                    total+=3
                elif gg=='4 = VERY OFTEN':
                    total+=4
            if total>r1:
                pp="VERY HIGH! -----> That's bad!"
            elif total<r2:
                pp="VERY LOW! -----> WOW Great!"
            elif total==mid:
                pp="MODERATE! -----> Not a problem!"
            elif total<mid and total>=mid-d:
                pp="MODERATELY LOW! -----> Nice one!"
            elif total>mid and total<=mid+d:
                pp="MODERATELY HIGH! -----> Take care!"
            elif total>mid+d and total<=r1:
                pp="HIGH! -----> Need to chill!"
            elif total<mid-d and total>=r2:
                pp="LOW! -----> Good one!"
            PSC1=[0]
            bot.sendMessage(ms['chat']['id'],'\nHey! You just finished your test!! Let me get you the score!\n\nSo, answer :-- '+str(total)+' out of 40 ! and your STRESS LEVEL is -- '+pp+'\n\n~ DARK',reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Wanna Try Again??'),KeyboardButton(text='No Thanks!')]]))
        if start!=0:
            start+=1

bot.message_loop(main)
while 1:
    time.sleep(10)
    
''' CODED BY TSG405(0) '''
