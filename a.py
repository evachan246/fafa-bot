import logging
import random
import telegram
import cv2
import requests

from xml.etree import ElementTree
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import User, InlineKeyboardMarkup
import os
PORT = int(os.environ.get('PORT', 5000))
TEMP = 0
List = []
imgList = []
H = []

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



def image_handlertesting(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('image.jpg')
    imgD = cv2.imread("image.jpg",0)
    photo = cv2.calcHist([imgD], [0], None, [256], [0, 256])
    photo = cv2.normalize(photo, photo, 0, 1, cv2.NORM_MINMAX, -1)

    for i in range(3):
        name = "resource/img"+(i+1)+".jpg"
        imgList[i] = cv2.imread("resource/img"+(i+1)+".jpg",0)
        H[i] = cv2.calcHist([imgList[i]], [0], None, [256], [0, 256])
        H[i] = cv2.normalize(H[i], H[i], 0, 1, cv2.NORM_MINMAX, -1)
    for i in range(3):
        if(cv2.compareHist(photo, H[i], 0)>=0.8):
            context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
            context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id = update.message.from_user.id)
            break


def image_handler(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('image.jpg')
    imgD = cv2.imread("image.jpg",0)
    photo = cv2.calcHist([imgD], [0], None, [256], [0, 256])
    photo = cv2.normalize(photo, photo, 0, 1, cv2.NORM_MINMAX, -1)

    img1 = cv2.imread("resource/img1.jpg",0)
    H1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)

    img2 = cv2.imread("resource/img2.jpg",0)
    H2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)

    img3 = cv2.imread("resource/img3.jpg",0)
    H3 = cv2.calcHist([img3], [0], None, [256], [0, 256])
    H3 = cv2.normalize(H3, H2, 0, 1, cv2.NORM_MINMAX, -1)

    if(cv2.compareHist(photo, H1, 0)>=0.8 or cv2.compareHist(photo, H2, 0)>=0.8 or cv2.compareHist(photo, H3, 0)>=0.8):
        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
        context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id = update.message.from_user.id)

def docmsg(update, context):
    if update.message.document.mime_type == "video/mp4":
        #context.bot.sendMessage(chat_id=update.message.chat.id,text = "This is a GIF!")
        file2 = context.bot.getFile(file_id=update.message.file_id)
        #context.bot.sendMessage(chat_id=update.message.chat.id,text = "Get ")
        file2.download('image.gif')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def checkTemp(update, context):
    #context.bot.sendMessage(chat_id=update.message.chat.id, text=str("TEST1"))
    response = requests.get("https://rss.weather.gov.hk/rss/CurrentWeather.xml")
    #context.bot.sendMessage(chat_id=update.message.chat.id,text = str("TEST2"))
    tree = ElementTree.fromstring(response.content);
    #context.bot.sendMessage(chat_id=update.message.chat.id,text = str("TEST3"))
    textTem = tree[0][7][6].text
    arraytemp = textTem.split('\n')
    for x in arraytemp:
        if(x.find("Air temperature")>=0) :
            realTemp = x.split()
            for y in realTemp:
                if(is_number(y)):
                    update.message.reply_text('今日天氣溫度係' +y+'度')

def dllmcount(update, context):
    message = (update.message.text).lower()
    increaseTemp = 0
    if(update.message.reply_to_message.from_user.id is not None):
        if "dllm"  in message:
            target = update.message.reply_to_message.from_user.id
            update.message.reply_text(target)
    count = 0
    
        
    

def main():
    """Start the bot."""
    
    TOKEN = os.environ['TOKEN']
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    #dp.add_handler(CommandHandler("help", help_command))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(CommandHandler("checkTemp", checkTemp))
    dp.add_handler(MessageHandler(Filters.sticker , go))
    dp.add_handler(MessageHandler(Filters.photo , image_handler))
    dp.add_handler(MessageHandler(Filters.document, docmsg))
    dp.add_handler(MessageHandler(Filters.text, dllmcount))
    
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
