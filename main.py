import telebot
import sqlite3 as sq
from telebot import types

bot = telebot.TeleBot('7155989263:AAFcqabkraoHUo7DnPQsi51Fh0kBPXk6Vrg')
name = None
age = None
gender = None
AboutMe = None


@bot.message_handler(commands=['start'])
def start(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name, age, gender, AboutMe )')

    con.commit()

    bot.send_message(message.chat.id, 'Привет , давай создадим новый аккаунт! Введите ваше имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()

    bot.send_message(message.chat.id, 'Введите ваш возраст!')
    bot.register_next_step_handler(message, user_age)

def user_age(message):
    global age
    age = message.text.strip()

    bot.send_message(message.chat.id, '''Ваш пол?
    1.Мужской
    2.Женский''')

    bot.register_next_step_handler(message, user_gender)

def user_gender(message):
    global gender
    gender = message.text.strip()

    bot.send_message(message.chat.id, 'Расскажите немного про себя')
    bot.register_next_step_handler(message, user_AboutMe)

def user_AboutMe(message):
    global AboutMe
    AboutMe = message.text.strip()

    bot.send_message(message.chat.id, 'Отличная анкета получилось')


    with sq.connect('G!Friends.db', check_same_thread=False) as con:
        cur = con.cursor()

        cur.execute("INSERT INTO users (name, age, gender, AboutMe ) VALUES ('%s','%s','%s','%s')" % (name, age, gender, AboutMe))
        con.commit()
      #  cur.close()
       # con.close()

    bot.register_next_step_handler(message, user_FinReg)

def user_FinReg(message):


        bot.send_message(message.chat.id, 'Все верно?')
        bot.register_next_step_handler(message, menu)

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,
'''
1.Смотреть анкеты.
2.Заполнить анкету заново.
3.Изменить фото/видео.
4.Изменить текст анкеты.
    ''')
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    markup.row(btn1, btn2, btn3, btn4)









   # cur.execute('INSERT INTO users (name, age) VALUES ("%s","%s")' % (name, age))
   # conn.commit()
   # cur.close()
   # conn.close()




bot.polling(none_stop=True)

