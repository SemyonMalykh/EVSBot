import telebot
from telebot import types
import datetime
import db_interface

#Bot is made for Extreme sports club of the Higher School of Economics
#by Semyon Malykh
#https://vk.com/twilight_phantom
#malykhsm@gmail.com
#Uses pyTelegramBotAPI
#Actual version of Telegram Bot API - 3.5
#Bot gives an information about club itself and club events

token = '540230588:AAHL4lyAW1rKqSmzxF8b_-MxvBWCGOflD-Q'

bot = telebot.TeleBot(token)

#removes reply keyboard
@bot.message_handler(commands = ['wait'])
def wait(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Если я понадоблюсь, введи /hey', reply_markup=markup)

#awakes bot
@bot.message_handler(commands = ['hey'])
def awake(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    first_button = types.KeyboardButton('Про ЭВС')
    second_button = types.KeyboardButton('О мероприятиях')
    markup.row(first_button, second_button)
    bot.send_message(message.chat.id, 'Могу рассказать про ЭВС и о мероприятиях', reply_markup=markup)

@bot.message_handler(func=lambda message: (message.text == 'Привет' or message.text == 'привет'))
def awake_with_hello(message):
    markup = types.ReplyKeyboardMarkupReplyKeyboardMarkup(one_time_keyboard=True)
    first_button = types.KeyboardButton('Про ЭВС')
    second_button = types.KeyboardButton('О мероприятиях')
    markup.row(first_button, second_button)
    bot.send_message(message.chat.id, 'Могу рассказать про ЭВС и о мероприятиях', reply_markup=markup)

#answer to /start command and first message also
@bot.message_handler(commands=['start'])
def hello(message):
    hello_world = ('Привет! Спасибо, что добавил меня 😊\n'
                  'Я - бот клуба Экстремальные Виды Спорта ВШЭ\n'
                  'Я могу рассказать о нашем клубе и о мероприятиях, которые мы проводим ⛷🏇🏄\n'
                  'Чтобы общаться со мной, пожалуйста, нажимай кнопки ▶️\n'
                  'Разбудить меня можно, введя /hey, остановить - ⏸️\n'
                  'Начнём?\n')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    upper_button = types.KeyboardButton('Погнали! 💃')
    lower_button = types.KeyboardButton('Не сейчас ✋️')
    markup.row(upper_button)
    markup.row(lower_button)
    bot.send_message(message.chat.id, hello_world, reply_markup=markup)
    if not db_interface.is_user_in_db(message.chat.id):
        db_interface.add_new_user(message.chat.id, ' ')

#answer to 'Не сейчас'
@bot.message_handler(func=lambda message: (message.text == 'Не сейчас ✋️' ))
def not_now_reply(message):
    bot.send_message(message.chat.id, 'Ok! Если я понадоблюсь, набери /hey')

#answer to 'Погнали'
@bot.message_handler(func=lambda message: (message.text == 'Погнали! 💃' ))
def not_now_reply(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    first_button = types.KeyboardButton('Про ЭВС')
    second_button = types.KeyboardButton('О мероприятиях')
    markup.one_time_keyboard = True
    markup.row(first_button)
    markup.row(second_button)
    bot.send_message(message.chat.id, 'О чём рассказать?', reply_markup=markup)

@bot.message_handler(func=lambda message: (message.text == 'Про ЭВС' ))
def send_es_info(message):
    es_info = ('Тебе интересен активный образ жизни? ' 
               'Тогда Клуб ЭВС откроет для тебя такие замечательные виды спорта как:' 
               'водный туризм, горный туризм, пеший туризм, скалолазание, альпинизм, ' 
               'горный велосипед, серфинг, дайвинг, кайтинг, верховая езда, горные лыжи, ' 
               'сноуборд, скейтинг и роликовые коньки, лонгборд, пейнтбол, вейкбординг, ' 
               'питбайк - и многие другие направления экстремального спорта и активного отдыха' 
               'Больше информации на нашей странице вк:' 
               'https://vk.com/xsportclub')
    bot.send_message(message.chat.id, es_info)
    bot.send_message(message.chat.id, 'О мероприятиях - /events')

@bot.message_handler(func=lambda message: (message.text == '/more_events' or message.text == 'О мероприятиях' or message.text == '/events' or message.text == 'Предстоящие события' or message.text == '/forthcoming_events'))
def send_events_info(message):
    events = db_interface.get_forthcoming_events()
    for id in events:
        event = db_interface.get_event_info(id)
        if event[4] > datetime.date.today():
            send = event[1] + '\n' + 'Даты: ' + event[4].strftime("%d/%m/%Y") + ' - ' + event[5].strftime("%d/%m/%Y") + '\n' + 'Место: ' +event[3] + '\n' + 'Больше информации - ' + event[7]
            bot.send_message(message.chat.id, send)

@bot.message_handler(func=lambda message: db_interface.event_is_in_db(message.text))
def send_events(message):
    event = db_interface.get_event_info_by_name(message.text)
    print(type(event), event)
    send = event[1] + '\n' + 'Даты: ' + event[4].strftime("%d/%m/%Y") +\
           ' - ' + event[5].strftime("%d/%m/%Y") + '\n' + 'Место: ' + event[3] + '\n' +\
            'Описание:\n' + event[2]
    bot.send_message(message.chat.id, send)
    bot.send_message(message.chat.id, 'Записаться - /enroll_to_' + event[7][1:])
    bot.send_message(message.chat.id, 'Ещё события - /forthcoming_events')

#answer to thanks
@bot.message_handler(func=lambda message: (message.text == 'Спасибо' or message.text == 'спасибо'))
def echo_all(message):
    bot.send_message(message.chat.id, 'Рад помочь! 😊️')


@bot.message_handler(func=lambda message: ('/enroll_to' in message.text ))
def enroll_to_event(message):
    event_name = '/' + message.text[11:]
    event_id = db_interface.get_event_id_by_name(event_name)
    organizer_id = db_interface.get_event_organizer(event_id)
    if not db_interface.is_user_registred(message.chat.id, event_id):
        db_interface.enroll_user_to_event(message.chat.id, event_name)
        bot.send_message(message.chat.id, 'Спасибо за запись! ✅\nВ ближайшее время напишет организатор')
        bot.send_message(message.chat.id, 'Ещё события - /forthcoming_events')
        bot.send_message(organizer_id, 'На ' + event_name + ' записался новый человек!\nСвяжись с ним пожалуйста ')
        bot.forward_message(organizer_id, message.chat.id, message.message_id)
    else:
        bot.send_message(message.chat.id, 'Вы уже записаны на это мероприятие')

#send_help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Чтобы разбудить меня, введи /hey \n'
                                      'Чтобы приостановить, введи /wait')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Прости, я пока не понимаю текст. Введи /hey')

bot.polling()
