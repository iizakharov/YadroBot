import telebot
import random
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    stickers = open('static/help.tgs', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Школьное расписание')
    item2 = types.KeyboardButton('Расписание походов в КЮП')

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "<b>Привет</b>".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
    bot.send_sticker(message.chat.id, stickers)


@bot.message_handler(content_types=['text'])
def KYF_School(message):
    if message.chat.type == 'private':
        if message.text == 'Школьное расписание':
            markup = types.InlineKeyboardMarkup(row_width=2)

            item1 = types.InlineKeyboardButton("Текст", callback_data='text')
            item2 = types.InlineKeyboardButton("Фото", callback_data='teer')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Ок,Текст или Фото ?",
                             reply_markup=markup)

        elif message.text == 'Расписание походов в КЮП':

            bot.send_message(message.chat.id,
                             "Понедельник 18:50\nВторник ---\nСреда 18:50\nЧетверг ---\nПятница 18:50")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    def get_name(message):
      name = message.text
      bot.send_message(call.message.chat.id, name)
    try:
        if call.message:
            if call.data == 'text':
                markup = types.InlineKeyboardMarkup(row_width=2)

                item1 = types.InlineKeyboardButton("Понедельник",
                                                   callback_data='pn')
                item2 = types.InlineKeyboardButton("Вторник",
                                                   callback_data='vt')
                item3 = types.InlineKeyboardButton("Среда", callback_data='sr')
                item4 = types.InlineKeyboardButton("Четверг",
                                                   callback_data='ht')
                item5 = types.InlineKeyboardButton("Пятница",
                                                   callback_data='pt')

                markup.add(item1, item2, item3, item4, item5)

                bot.send_message(call.message.chat.id, 'День недели ?',
                                 reply_markup=markup)

            elif call.data == 'teer':

                bot.send_message(call.message.chat.id, '<b>Ок держи!</b>',
                                 parse_mode='html')

                # bot.send_photo(c.chat_id, photo=("Raspisanie_urokov.")
            elif call.data == 'pn':

                bot.send_message(call.message.chat.id, 'День недели ?',
                                 reply_markup=None)
                bot.register_next_step_handler(call.message, get_name)

    except  Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)

{'content_type': 'text',
 'message_id': 991,
 'from_user': {'id': 1140597464,
               'is_bot': True,
               'first_name': 'myTestBot',
               'username': 'cofevil_bot',
               'last_name': None,
               'language_code': None},
 'date': 1595358035,
 'chat': {'type': 'private',
          'last_name': 'Zakharov',
          'first_name': 'Ilya',
          'username': 'Axeska',
          'id': 220294570,
          'title': None,
          'all_members_are_administrators': None,
          'photo': None,
          'description': None,
          'invite_link': None,
          'pinned_message': None,
          'sticker_set_name': None,
          'can_set_sticker_set': None},
 'forward_from_chat': None,
 'forward_from_message_id': None,
 'forward_from': None,
 'forward_date': None,
 'reply_to_message': None,
 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': 'Ты расскажешь или я?', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None,
 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None,
 'json': {'message_id': 991,
          'from': {'id': 1140597464,
                   'is_bot': True,
                   'first_name': 'myTestBot',
                   'username': 'cofevil_bot'},
          'chat': {'id': 220294570,
                   'first_name': 'Ilya',
                   'last_name': 'Zakharov',
                   'username': 'Axeska',
                   'type': 'private'},
          'date': 1595358035,
          'text': 'Ты расскажешь или я?',
          'reply_markup': {'inline_keyboard': [[{'text': 'Рассказать', 'callback_data': 'add_joke'}, {'text': 'Послушать', 'callback_data': 'get_joke'}]]}}}
