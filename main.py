import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('7155989263:AAFcqabkraoHUo7DnPQsi51Fh0kBPXk6Vrg')
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('G!Friends.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name TEXT, age INTEGER, gender TEXT, AboutME Text )')
   # cur.execute('CREATE TABLE IF NOT EXISTS users_preference (id int auto_increment primary key,gender_preference TEXT, age_min INTEGER, age_max INTEGER, FOREIGN KEY (id) REFERENCES users (id)')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет , давай создадим новый аккаунт! Введите ваше имя! ')
    bot.register_next_step_handler(message, user_name)


    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    markup.row(btn1, btn2, btn3, btn4)
    #bot.send_message(message.chat.id, 'Привет , давай создадим новый аккаунт! '+ message.from_user.first_name, reply_markup = markup)
    bot.send_message(message.chat.id,
'''
1.Смотреть анкеты.
2.Заполнить анкету заново.
3.Изменить фото/видео.
4.Изменить текст анкеты.
    ''')

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш возраст! ')
    bot.register_next_step_handler(message, user_age)

def user_age(message):
    age = message.text.strip()

    conn = sqlite3.connect('G!Friends.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, age) VALUES ("%s","%s")' % (name, age))
    conn.commit()
    cur.close()
    conn.close()





@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, 'Help!')

@bot.message_handler(commands=['userId'])
def userId(message):
      bot.send_message(message.chat.id, 'Help!')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Фото')


bot.polling(none_stop=True)