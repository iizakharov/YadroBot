from datetime import datetime, timedelta
import config
import telebot
from telebot import types
from database import db

bot = telebot.TeleBot(config.TOKEN)
user = ''
counter = 0
user_mes_count = {
    'user_id': 0,
    'count_mes': 0
}
mute_time = ''


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/hello.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #  клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(u"\U0001F4A3")
    item2 = types.KeyboardButton('Анекдот')
    item3 = types.KeyboardButton('Ближайший повд выпить')
    item4 = types.KeyboardButton(u"\U0001F633")
    item5 = types.KeyboardButton(u"\U0001F595\U0001F3FD")

    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Какие люди в Голливуде!?'
                                      '\n{0.first_name}, я - <b>{1.first_name}'
                                      '</b>, бот созданный чтобы быть'
                                      ' полезным ;) '.format(message.from_user,
                                                             bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def welcome(message):
    sti = open('static/help.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, '{0.first_name}, тут всё просто!'
                                      '\nЕсли хочешь поработать, напиши в'
                                      ' чат:\n/start\n и тогда пообщаемся {1}'
                     .format(message.from_user, u"\U0001F618"),
                     parse_mode='html')


@bot.message_handler(content_types=['sticker'])
def stick_answer(message):
    global user_mes_count
    global counter
    global mute_time
    counter += 1
    if counter > 3:
        # print(mute_time.strftime("%H:%M:%S"))
        # print(datetime.now().strftime("%H:%M:%S"))
        if mute_time < datetime.now():
            counter = 1
    user_mes_count = {message.from_user.id: counter}
    print(user_mes_count)
    if user_mes_count.get(message.from_user.id) == 1:
        bot.send_message(message.chat.id, 'Cтикер - ЗАЧЁТ!! Не зря в Телеге '
                                          'сидим {0}'.format(u"\U0001F600"))
    elif user_mes_count.get(message.from_user.id) == 2:
        bot.send_message(message.chat.id, 'Этот тоже ничего {0}'.format(u"\U0001F600"))
    elif user_mes_count.get(message.from_user.id) == 3:
        bot.send_message(message.chat.id, 'Отъебись!')
        mute_time = datetime.now() + timedelta(minutes=5)
    elif user_mes_count.get(message.from_user.id) == 10:
        bot.send_message(message.chat.id, 'Тебя бы забанить за такое! {0}'.format(u"\U0001F600"))


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.type == 'private' or message.chat.type == 'group' or message.chat.type == 'supergroup' or message.chat.type == 'channel':
        if message.text == u"\U0001F4A3":
            bot.send_message(message.chat.id, 'пока тут пусто {0}'
                             .format(u"\U0001F648"))
        elif message.text == 'Анекдот':
            global user
            user = message.from_user.first_name
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Рассказать',
                                               callback_data='add_joke')
            item2 = types.InlineKeyboardButton('Послушать',
                                               callback_data='get_joke')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Ты расскажешь или я?',
                             reply_markup=markup)

        elif message.text == 'Ближайший повд выпить':
            near_date = db.get_bdate()
            bot.send_message(message.chat.id, 'Скоро, через {1} дня(ей) днюха у нашего {0}, т.к. он родился {2}'
                             .format(near_date[0], near_date[1], near_date[2]))
            # bot.send_message(message.chat.id, 'пока тут пусто {0}'
            #                  .format(u"\U0001F648"))
        elif message.text == u"\U0001F633":
            bot.send_message(message.chat.id, 'пока тут пусто {0}'
                             .format(u"\U0001F648"))
        elif message.text == u"\U0001F595\U0001F3FD":
            bot.send_message(message.chat.id, 'пока тут пусто {0}'
                             .format(u"\U0001F648"))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    def new_joke(message):
        # print(message.text)
        if len(message.text) <= 20:
            bot.send_message(call.message.chat.id, 'Это какая-то шляпа! Нормально делай - нормально будет!')
        else:
            db.add_joke(message.text)
            bot.send_message(call.message.chat.id, 'Недаюсь всем понравится, '
                                                   'а не только тебе ;)')
    try:
        if call.message:
            if call.data == 'add_joke':
                markup = types.InlineKeyboardMarkup(row_width=2)

                item1 = types.InlineKeyboardButton("Я передумал",
                                                   callback_data='exit')
                markup.add(item1)
                bot.send_message(call.message.chat.id, 'Напиши свой анекдот!',
                                 reply_markup=markup)
                bot.register_next_step_handler(call.message, new_joke)

            elif call.data == 'exit':
                bot.send_message(call.message.chat.id,
                                 'Сначала придумай, потом кликай ;)',
                                 reply_markup=None)
            elif call.data == 'get_joke':
                global user
                joke = db.get_joke()
                bot.send_message(call.message.chat.id, 'Специально для {0}:\n{1}'.format(user, str(joke)),
                                 parse_mode='html')


    except Exception as e:
        print('Ошибка callback_query: ' + repr(e))
        # logger.error('Ошибка callback_query: ' + repr(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)
