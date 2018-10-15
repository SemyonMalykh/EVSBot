import telebot
import schedule
#The MIT License (MIT)
#Copyright (c) 2013 Daniel Bader (http://dbader.org)
import time
import db_interface


token = '540230588:AAHL4lyAW1rKqSmzxF8b_-MxvBWCGOflD-Q'

bot = telebot.TeleBot(token)

def send_notifications():
    events = db_interface.events_tomorrow()
    for event in events:
        users = db_interface.enrolled_users(event)
        for user in users:
            bot.send_message(user, 'Привет! Это бот ЭВС✌️\nНапоминаю, что завтра состоится мероприятие:\n' + db_interface.get_event_name(event))


schedule.every(1440).minutes.do(send_notifications)

while True:
    schedule.run_pending()
    time.sleep(1)

