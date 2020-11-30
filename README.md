# TELEGRAM-BOT
Program and compute a TELEGRAM-BOT,  @http://t.me/TSGDARKBOT @http://t.me/TSG_Stress_Bot

For local server, just need to run the program in any editor with the TELEGRAM API TOKEN. (Don't forget to PIP install the required modules!)


## STEPS for CREATING, WEB HOSTING and DEPLYING A BOT online!

### Creating a bot
So, the first thing you need to do is to, tell Telegram that you want to create a bot. For this, you’ll need a "Telegram" account – Install their application on your phone, and get it fired up!

Next, start a conversation with the “BotFather”. This is a bot that --Telegram-- themselves run, and it controls the creation and registration of bots on their platform. On the Android version of their app, here’s what you do (other platforms are similar)

    Tap on the start conversation button in the bottom right to start a new conversation.
    Tap the magnifying glass “Search” icon near the top right.
    Type “botfather”.
    Tap on the “@BotFather” that appears. Make sure it has a blue checkmark next to it
    It will display a welcome message.
    Click the “Start” button.
    Send a message “/newbot”
    It will ask for a name for your bot. I’m going to call mine “DARK” but you should choose a name that’s unique to you.
    Next it will ask for a username; I’ll use “TSGDarkBot”
    If all goes well, it will print out a message telling you that the bot was created. There’s one important bit of information in there, that you’ll need for later: the "token" to access the HTTP API. It will be a long string of alphanumeric characters, maybe with a colon in it. To keep this for later, I copied the message on my ipad – not super-secure, but probably safe enough if you’re not going to be putting anything secret into your bot.

Right! so let’s check that your bot is created, even if it’s currently not very talkative or active. Start a conversation with it, using the same method to start a chat as you did with the BotFather. You’ll be able to find it and start a chat, but when you click the “Start” button, nothing will happen :(

### A first simple bot!

On your computer:

    I recommend you create a new PythonAnywhere account for this tutorial – we’ll be creating a website later, and if you already have a website, we don’t want to get confused between the two. You can have multiple free accounts, even using the same email address, so there’s no harm in signing up for a new one. Just create a free “Beginner” one!

    >> Start a “Bash” console

    In there, run:
    $ pip3.6 install telepot --user
    
    this will install (for your own PythonAnywhere account) the excellent telepot Python library, which hides some of the complexities of talking to Telegram’s API. Wait for the process to complete.

Next, click the "PythonAnywhere logo" to the top left, to go back to the PythonAnywhere Dashboard.

Go to the “Files” tab.

In the “Enter new file name” tab, type a filename ending with “.py” for your bot’s code – say, bot.py – and click the “New file” button.

Enter the following code, replacing “YOUR_AUTHORIZATION_TOKEN” with the token that the BotFather gave you earlier:

-------------------------------------------------------------------------------------------------------------------

import urllib3
import telepot
import time

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
'''
Required for FREE Pythonanywhere Account only (BEGINNER)!
'''

bot = telepot.Bot('<YOUR_TELEGRAM_AUTHORIZATION_TOKEN>')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        bot.sendMessage(chat_id, "You said --> '{}'".format(msg["text"]))

bot.message_loop(handle)

while 1:
    time.sleep(20)
    
-------------------------------------------------------------------------------------------------------------------
 
Click the “»> Run this file” button in the page.

YAY! A working bot!!! :D
Let’s work through that Code bit by bit.....

    #!/usr/bin/python3.6
This tells PythonAnywhere that you want to run the code using Python 3.6, which is the version of Python we installed telepot for.

    import telepot
    import time
    import urllib3
This bit just imports the Python modules that we’re going to use.


    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
Like the comments say, this stuff is only needed if you’re using a free “Beginner” PythonAnywhere account – we are, of course, for this tutorial, but you can remove it if you want to reuse the code in a paid account later. It’s there because free accounts can only connect outwards to particular external websites, and those connections have to go through a proxy server. Many APIs pick up the details of the proxy server automatically from their system environment when they’re running, but telepot doesn’t. It’s not a problem, it just means we have to be a bit more explicit and say “use this proxy over here!”.

    bot = telepot.Bot('YOUR_AUTHORIZATION_TOKEN')
Now we get to the core of the code. This line uses telepot to connect to Telegram’s server.

Next, we define a function that knows how to handle messages from Telepot.

    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
The first thing we do is pull the useful information out of the message, using telepot’s glance utility function.

    print(content_type, chat_type, chat_id)
…we print out some of the information, just for debugging purposes...

    if content_type == 'text':
    	  bot.sendMessage(chat_id, "You said '{}'".format(msg["text"]))
We only handle text messages for the time being; speech recognition is a bit outside the bounds of this tutorial… When we get a text message, we simply reply back telling the person, what they said.

So that’s the end of the message-handler function. Back to the main code:
    
    bot.message_loop(handle)
This tells telepot to start running a message loop. This is a background thread that will keep running until the program exits; it listens on the connection that was opened to Telegram and waits for incoming messages. When they come in, it calls our handle function with the details.

    while 1:
        time.sleep(20)
And then we wait forever.................. Like I said, the telepot message loop will only keep running until our program exits, so we want to stop it from exiting.

So now we have a working bot and we know how it works. Let’s make it better!! >>>>>>>>>


### Moving to WebHooks

The bot that you have right now is just running inside the console underneath your editor (LOCAL IP SERVER). It will actually keep running for quite a while, but if PythonAnywhere do any system maintenance work that requires restarting the server it’s on, it will stop and not restart. That’s obviously not much good for a bot, so let’s fix it.

What we’ll use is the -- Telegram’s “webhooks” API. Webhooks are a different way of connecting to Telegram. Our previous code made an out-bound connection from PythonAnywhere to Telegram, then relied on Telegram sending messages down that connection for processing. With webhooks, things are reversed. We essentially tell Telegram, “when my bot receives a message, connect to PythonAnywhere and pass on the message”. And the “connect to PythonAnywhere” bit is done by creating a web application to run inside your PythonAnywhere account that will serve a really simple API.

If any of that sounds daunting, don’t worry. It’s actually pretty simple, and the instructions are detailed :-)

    Click on the PythonAnywhere logo to go back to the PythonAnywhere dashboard.
    On the “Consoles” tab, click on the small “X” next to the “firstsimplebot.py” console. This is important – it will kill the running bot that we’ve already created so that it doesn’t interfere with the the new one we’re about to create.
    Go to the “Web” tab.
    Click the “Add a new web app” button.
    The first page will just tell you that the web app will be hosted at your-pythonanywhere-username.pythonanywhere.com. Click next.
    On the next page, choose the “Flask” web framework. Flask is a great choice for simple websites that are designed for APIs.
    On the next step, choose “Python 3.6”. That’s the version we installed telepot for.
    On the next page, just accept the default location for your Flask app. It will be something like /home/your-pythonanywhere-username/mysite/flask_app.py
    After a short wait, you’ll see an “All done!” message and your website will be set up. There will be a link to it – follow the link and you should see a message saying “Hello from Flask!”

So now you have a simple website running that just displays one message. What we need to do next is configure it so that instead, it’s running an API that Telegram can connect to. And we also need to tell Telegram that it’s there, and which bot it’s there to handle.

    Click your browser’s “Back” button to go back to the “Web” tab.
    Look down the page a bit, and you’ll see the “Code” section.
    In that section, open the “Go to directory” link for the “Source code” in a new browser tab. (It’ll be useful to keep the “Web” tab around for later.)
    In the new tab, you’ll see the “Files” page. One file will be called “flask_app.py”; click on it to go to the editor.

Enter the following code. Don’t worry about what it does yet, we’ll go through that in a second. But don’t forget to replace YOUR_AUTHORIZATION_TOKEN with your Telegram HTTP API token, and YOUR_PYTHONANYWHERE_USERNAME with your PythonAnywhere username. Also replace A_SECRET_NUMBER with a number that only you know; a good way to get one that’s properly random is to go to this online GUID generator, which will generate a unique number like “c04a4995-jkdsfhsdfgyufwjkkl-fopf51”.


----------------------------------------------------------------------------------------------------------------------------------------------------------
       
    from flask import Flask, request
    import telepot
    import urllib3

    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

    secret = "A_RANDOM_SECRET_NUMBER"
    bot = telepot.Bot('YOUR_AUTHORIZATION_TOKEN')
    bot.setWebhook("https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/{}".format(secret), max_connections=1)

    app = Flask(__name__)

    @app.route('/{}'.format(secret), methods=["POST"])
    def telegram_webhook():
     update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            bot.sendMessage(chat_id, "From the web: you said --> '{}'".format(text))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message!!")
    return "OK"

----------------------------------------------------------------------------------------------------------------------------------------------------------
Once you’ve entered the code and made sure you’ve made the three substitutions:

    Save the file
    Switch to the browser tab with your web app setup in it.
    Click the green “Reload” button near the top.
    Wait for the “spinner” to finish.

Back on your phone/i-pad, send another message. This time you should get a message back saying clearly that it came from the web. So now we have a bot using webhooks!

Let’s work through the code now:


    from flask import Flask, request
    import telepot
    import urllib3

So again, we import some Python modules. This time as well as the telepot and the urllib3 stuff that we need to talk to Telegram, we use some stuff from Flask.

    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
    
Once again, the stuff we need to access Telegram from a free PythonAnywhere account.

    secret = "A_RANDOM_SECRET_NUMBER"
    
Now, this is a bit of best-practice for Telegram bots using webhooks. Your bot is running as a publicly-accessible website. Anyone in the world could connect to it. And of course we really don’t want random people to be able to connect, pretending to be Telegram, and make it say inappropriate things… so, we’re going to say that the website only serves up one page, and the URL for that page is unguessable. This should make things reasonably safe. You’ll see the code for that in a moment.

    bot = telepot.Bot('YOUR_AUTHORIZATION_TOKEN')
    
We connect to Telegram using telepot, just like we did before.

    bot.setWebhook("https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/{}".format(secret), max_connections=1)

We use telepot to send a message to Telegram saying “when my bot gets a message, this is the URL to send stuff to”. This, of course, not only contains the host name for your website with your PythonAnywhere username, it also includes the hopefully-unguessable secret that we defined earlier. It’s also worth noting that it uses secure HTTPS rather than HTTP – all websites on PythonAnywhere, even free ones, get HTTPS by default, and Telegram (quite sensibly) will only send webhooks over HTTPS.

    app = Flask(__name__)
Now we create a Flask application to handle requests.

    @app.route('/{}'.format(secret), methods=["POST"])
    def telegram_webhook():
This is some Flask code to say “when you get a POST request on the secret URL, run the following function”.

    update = request.get_json()
Telegram sends stuff to bots using JSON encoding, so we decode it to get a Python dictionary.

So now we have, and hopefully understand, a simple Telegram bot that will keep running pretty much forever! Websites on PythonAnywhere free accounts last for three months, and then you can extend them for another three months – and three months later you can extend again, and so on, as many times as you like. So as long as you’re willing to log in to PythonAnywhere four times a year, you’re all set :-)
