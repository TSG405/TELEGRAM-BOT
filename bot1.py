import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
   
    update.message.reply_text('Hi User!')


def help(update, context):
    
    update.message.reply_text('Help!')


def echo(update, context):
    
    update.message.reply_text(update.message.text)


def error(update, context):
    
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    
    updater = Updater("TOKEN", use_context=True)

    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    
    dp.add_handler(MessageHandler(Filters.text, echo))

   
    dp.add_error_handler(error)

 
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
