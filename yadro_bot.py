from datetime import datetime, timedelta
import config
import telebot
from telebot import types
from database import db
from database.db import create_table_bday, create_table, new_member

from log.decos import log

bot = telebot.TeleBot(config.TOKEN)

counter = 0
user_mes_count = {
    'user_id': 0,
    'count_mes': 0
}
mute_time = ''


@log
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


@log
@bot.message_handler(commands=['help'])
def f_help(message):
    sti = open('static/help.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, '{0.first_name}, тут всё просто!'
                                      '\nЕсли хочешь поработать, напиши в'
                                      ' чат:\n/start\n и тогда пообщаемся {1}'
                     .format(message.from_user, u"\U0001F618"),
                     parse_mode='html')


@log
@bot.message_handler(commands=['joke'])
def add_joke(message):
    bot.send_message(message.chat.id, '{0.first_name}, напиши анекдот'
                                      ' и я его добвлю {1}'
                     .format(message.from_user, u"\U0001F618"),
                     parse_mode='html')
    bot.register_next_step_handler(message, new_joke)


@log
def new_joke(message):
    if len(message.text) <= 20:
        bot.send_message(message.chat.id, 'Это какая-то шляпа!'
                                          ' Нормально делай -'
                                          ' нормально будет!')
    else:
        db.add_joke(message.text)
        bot.send_message(message.chat.id, 'Недаюсь всем понравится, '
                                          'а не только тебе ;)')


@log
@bot.message_handler(commands=['addmember'])
def add_member(message):
    bot.send_message(message.chat.id, 'Имя и фамилия в родительском падеже',
                     parse_mode='html')
    bot.register_next_step_handler(message, add_bdate)


def add_bdate(message):
    member_name = message.text
    _date = bot.send_message(message.chat.id, 'Дата рождения в формате: гггг-мм-дд',
                             parse_mode='html')
    bot.register_next_step_handler(message, lambda m: add_to_base(m, member_name))


def add_to_base(message, date):
    new_member(date, message.text)
    bot.send_message(message.chat.id, 'Готово! '
                                      '\n Дабавлено напоминание для {0}'
                                      ' с датой роджения: {1}'
                     .format(date, message.text),
                     parse_mode='html')


@log
def new_joke(message):
    if len(message.text) <= 20:
        bot.send_message(message.chat.id, 'Это какая-то шляпа!'
                                          ' Нормально делай -'
                                          ' нормально будет!')
    else:
        db.add_joke(message.text)
        bot.send_message(message.chat.id, 'Недаюсь всем понравится, '
                                          'а не только тебе ;)')


@log
@bot.message_handler(commands=['createdbpls'])
def welcome(message):
    create_table_bday()
    create_table()
    bot.send_message(message.chat.id, 'Готово!', parse_mode='html')


@log
@bot.message_handler(content_types=['sticker'])
def stick_answer(message):
    global user_mes_count
    global counter
    global mute_time
    counter += 1
    if counter > 3:
        if mute_time < datetime.now():
            counter = 1
    user_mes_count = {message.from_user.id: counter}
    print(user_mes_count)
    if user_mes_count.get(message.from_user.id) == 1:
        bot.send_message(message.chat.id, 'Cтикер - ЗАЧЁТ!! Не зря в Телеге '
                                          'сидим {0}'.format(u"\U0001F600"))
    elif user_mes_count.get(message.from_user.id) == 2:
        bot.send_message(message.chat.id, 'Этот тоже ничего {0}'
                         .format(u"\U0001F600"))
    elif user_mes_count.get(message.from_user.id) == 3:
        bot.send_message(message.chat.id, 'Отъебись!')
        mute_time = datetime.now() + timedelta(minutes=5)
    elif user_mes_count.get(message.from_user.id) == 10:
        bot.send_message(message.chat.id, 'Тебя бы забанить за такое! {0}'
                         .format(u"\U0001F600"))


@log
@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.type == 'private' or message.chat.type == 'group' or\
            message.chat.type == 'supergroup'\
            or message.chat.type == 'channel':
        if message.text == u"\U0001F4A3":
            bot.send_message(message.chat.id, 'пока тут пусто {0}'
                             .format(u"\U0001F648"))
        elif message.text == 'Анекдот':
            user_name = message.from_user.first_name
            joke = db.get_joke()
            bot.send_message(message.chat.id,
                             'Специально для {0}:\n{1}'.format(user_name,
                                                               str(joke)),
                             parse_mode='html')
        elif message.text == 'Ближайший повд выпить':
            near_date = db.get_bdate()
            bdate = near_date[2].split('-')
            _bdate = f'{bdate[2]}.{bdate[1]}'
            bot.send_message(message.chat.id, 'Скоро, через {1} дня(ей)'
                                              ' днюха у нашего {0},'
                                              ' т.e. {2} !'
                             .format(near_date[0], near_date[1], _bdate))
        elif message.text == u"\U0001F633":
            bot.send_message(message.chat.id, 'пока тут пусто {0}'
                             .format(u"\U0001F648"))
        elif message.text == u"\U0001F595\U0001F3FD":
            bot.send_message(message.chat.id, 'Сам пошёл! {0}'
                             .format(u"\U0001F595\U0001F3FD"))


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == 'add_joke':
#                 markup = types.InlineKeyboardMarkup(row_width=2)
#
#                 item1 = types.InlineKeyboardButton("Я передумал",
#                                                    callback_data='exit')
#                 markup.add(item1)
#                 bot.send_message(call.message.chat.id, 'Напиши свой анекдот!',
#                                  reply_markup=markup)
#                 bot.register_next_step_handler(call.message, new_joke)
#
#             elif call.data == 'exit':
#                 bot.send_message(call.message.chat.id,
#                                  'Сначала придумай, потом кликай ;)',
#                                  reply_markup=None)
#             elif call.data == 'get_joke':
#                 global user
#                 joke = db.get_joke()
#                 bot.send_message(call.message.chat.id, 'Специально для {0}:\n{1}'.format(user, str(joke)),
#                                  parse_mode='html')
#
#
#     except Exception as e:
#         print('Ошибка callback_query: ' + repr(e))
#         # logger.error('Ошибка callback_query: ' + repr(e))


bot.polling(none_stop=True)
