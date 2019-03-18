# -*- coding: cp1252 -*-
#import httplib2
import os
#import dropbox
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)



nphotos= 0
iduser = []
token = "874797436:AAH4uSbeoV_4nAAJHJG5fYvH_VzprMotR9U"


def cmd_help(bot, update):
  update.message.reply_text('Ayuda Bot Ayni')
  update.message.reply_text('Mensaje de ayuda')
def start(bot, update):
    global iduser
    user = update.message.from_user
    update.message.reply_text('BIENVENIDO/A A AYNI!')
    #update.message.reply_text('ESTAMOS REALIZANDO PRUEBAS A LA APLICACION DE DENUNCIAS URBANAS EN LA COMUNA DE ESTACION CENTRAL, POR FAVOR ENVIANOS FOTOS DE SITUACIONES DE RIESGO QUE PUEDAS DETECTAR MIENTRAS CAMINAS Y MANDA LA UBICACION DE CADA FOTO. MUCHAS GRACIAS')
    iduser.append (user.id)
    update.message.reply_text('Hola {}'.format(update.message.from_user.username)+'id:{}'.format(update.message.from_user.id))

    reply_keyboard = [['Si', 'No']]
    update.message.reply_text(
        'Hola! la emergencia actual corresponde a blablabla, deseas participar como voluntario?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    # logger.info(iduser)
    # logger.info(len(iduser))

    # db_string ="postgresql://pybossa:testerms@localhost/pybossams"
    # db = create_engine(db_string)
    meta = MetaData(db)
    usertelegram = Table('usertelegram', meta,
                       Column('name', String),
                       Column('chat_id', String))
    #db.execute= ("INSERT INTO usertelegram (name,chat_id) VALUES (user.first_name,user.id)")
    with db.connect() as conn:
        insert = usertelegram.insert().values(name=user.first_name,chat_id=user.id)
        conn.execute(insert)
    # new_user = UserTelegram(name=user.first_name,
    #                        chat_id=user.id)
    # usertelegram_repo.save(new_user)


def enviar_mensaje(mensaje):
    global iduser
    #bot.sendMessage(chat_id=iduser[0], text=mensaje)
    # global token
    # url = "https://api.telegram.org/bot" + token + "/sendMessage"
    # for x in iduser:
    #     params = {
    #     'chat_id': x,

    #     'text' : mensaje
    #     }

    # requests.post(url, params=params)

def hello(bot, update):
    update.message.reply_text('Hola {}'.format(update.message.from_user.first_name))


def photo(bot, update):
    global nphotos
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_name = str(user.id)+'_'+user.first_name+'_'+str(nphotos)+'.jpg'
    photo_file.download(photo_name)
    logger.info("Photo of %s %s: %s" % (user.id, user.first_name, photo_name))
    update.message.reply_text('Gracias por colaborar')
    #Subir imagen a dropbox
    # cliente = dropbox.Dropbox('iPxQjyn5VUAAAAAAAAAACRq_bzlxDdB_5vwbSIsBqKxKFZNMnDBBVgxbnBm-NNM3')
    # with open(photo_name, "rb") as f:
    #     cliente.files_upload(f.read(),'/'+photo_name, mute = True)
    #Sumar 1 al contador de imagenes
    nphotos = nphotos + 1
    #Eliminar imagen luego de subirla a dropbox
    os.remove(photo_name)

def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f" %(user.first_name, user_location.latitude, user_location.longitude))
    update.message.reply_text('Gracias por enviar su ubicación.')


updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hola', hello))
updater.dispatcher.add_handler(CommandHandler("ayuda", cmd_help))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))
updater.dispatcher.add_handler(MessageHandler(Filters.location, location))

updater.start_polling()
updater.idle()
