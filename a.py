import logging
import random
import telegram
import cv2

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import User, InlineKeyboardMarkup
import os
PORT = int(os.environ.get('PORT', 5000))
TEMP = 0
List = []

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start_command(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


#def echo(update, context):
#    """Echo the user message."""
#    text = update.message.text
#    if ( text.lower() =='dllm'):
#        update.message.reply_text('dllm')
#    if ( text.lower() == 'source'):
#        update.message.reply_text('here is the source link :'+
#        'https://connectpolyu-my.sharepoint.com/:f:/g/personal/18022038d_connect_polyu_hk/EoftV3mXfn9Em_HTMLRGWwkBIJHySPhJrKfn237Z5T3rtA?e=sggDys')

def echo(update, context):
    """Echo the user message."""
    x = update.message.from_user.id
    #print(x)
    if(x == 0):
       context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
    elif((update.message.text).lower() == 'dllm'):
        if(x != 81817865600):
            #context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
            x = update.message.from_user.id
            is_found =False
            for  i in range(len(List)):
                for j in range(len(List[i])):
                    if List[i][j] == x:
                        is_found = True
                        Temp = i
                        break
                if is_found:
                    List[Temp][1] += 1
                    if(List[Temp][1]%5==0):
                        context.bot.sendMessage(chat_id=update.message.chat.id,text = str(update.message.from_user.first_name)+' 唔好講粗口, 你講撚左 '+str(List[Temp][1])+' 次 ')
                    break
            if not is_found:
                List.append([x,1])

def go(update, context):
    x = update.message.from_user.id
    if( x == 0):
       update.message.reply_text(text = "賊")
    #y = update.message.sticker.file_id
    b = update.message.sticker.file_unique_id
    #print(b)
    if(b == 'AgADIwADO8nACw') :
        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

    
def image_handler(bot, update):    
    file = bot.getFile(update.message.photo[-1].file_id)
    update.message.reply_text("file_id: " + str(update.message.photo.file_id))
    


def main():
    """Start the bot."""
    TOKEN = '1312704556:AAE23BjzU1lL4SrREPqpdi6WNXSrb1z12f8'
    updater = Updater("1312704556:AAE23BjzU1lL4SrREPqpdi6WNXSrb1z12f8", use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command , echo))
    dp.add_handler(MessageHandler(Filters.sticker , go))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://fafa-tgbot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()