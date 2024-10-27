
import telebot
import sqlite3 as sq
from telebot import types

bot = telebot.TeleBot('7155989263:AAFcqabkraoHUo7DnPQsi51Fh0kBPXk6Vrg')
name = None
age = None
gender = None
city = None
AboutMe = None
downloaded_file = None




@bot.message_handler(commands=['start'])
def start(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,telegram_id INTEGER, name TEXT, age INTEGER, gender INTEGER, city TEXT, foto BLOB, AboutMe TEXT )')
    #cur.execute('DROP TABLE users')

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

    bot.send_message(message.chat.id, 'В каком городе вы хотите искать?')
    bot.register_next_step_handler(message, user_city)

def user_city(message):
     global city
     city = message.text.strip()

     bot.send_message(message.chat.id, 'Отправьте ваше фото')
     bot.register_next_step_handler(message, user_foto)

def user_foto(message):
    global downloaded_file
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)

    # Загружаем сам файл
    downloaded_file = bot.download_file(file_info.file_path)


    bot.send_message(message.chat.id, 'Расскажите немного о себе')
    bot.register_next_step_handler(message, user_AboutMe)


def user_AboutMe(message):
    global AboutMe
    AboutMe = message.text.strip()

  #  bot.send_message(message.chat.id, 'Отличная анкета получилось')
    user_FinReg(message)

   # with sq.connect('G!Friends.db', check_same_thread=False) as con:
    #    cur = con.cursor()

        #cur.execute("INSERT INTO users (name, age, gender, city, foto, AboutMe ) VALUES ('%s','%s','%s','%s','%s','%s')" % (name, age, gender, city, foto, AboutMe))
        #con.commit()

def user_FinReg(message):
        global downloaded_file
        bot.send_photo(message.chat.id, photo=downloaded_file)

        bot.send_message(message.chat.id, name + ', ' + age + ', '+ city + ', ' + AboutMe)
        bot.send_message(message.chat.id, 'Все верно?')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('1')
        btn2 = types.KeyboardButton('2')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
        '''
            1.ДА
2.НЕТ(заполнить анкету сначала)
        ''', reply_markup=markup)
        bot.register_next_step_handler(message, FReg)


@bot.message_handler(commands=['menu'])
def menuFirst(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
    '''
    1.Смотреть анкеты.
    2.Заполнить анкету заново.
    3.Изменить фото/видео.
    4.Изменить текст анкеты.
        ''',reply_markup=markup)
    bot.register_next_step_handler(message, menuSec)


@bot.message_handler(content_types=['menuSec_text'])
def menuSec(message):
    text = message.text

    if (text == "1"):
        search(message)
    elif (text == "2"):

        delete_user(telegram_id)

        bot.send_message(message.chat.id, 'Давай попробуем заново')
        start(message)

    elif (text == "4"):

        bot.send_message(message.chat.id, 'Расскажите немного о себе')

        bot.register_next_step_handler(message, newAboutMe)

    else:
        bot.send_message(message.chat.id, 'Нет такой функции')

def newAboutMe(message):
    global AboutMe

    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()

    AboutMe = message.text.strip()
    cur.execute('UPDATE users SET AboutMe = ? WHERE telegram_id = ?', (AboutMe, telegram_id))
    con.commit()

    user_FinReg(message)

@bot.message_handler(content_types=['FReg'])
def FReg(message):
    global telegram_id
    telegram_id = message.from_user.id
    text = message.text

    if (text == "1"):
        with sq.connect('G!Friends.db', check_same_thread=False) as con:
            cur = con.cursor()

            cur.execute(
                "INSERT INTO users (telegram_id, name, age, gender, city, foto, AboutMe ) VALUES (?,?,?,?,?,?,?);", (
                telegram_id, name, age, gender, city, downloaded_file, AboutMe))
            con.commit()
            menuFirst(message)

    elif (text == "2"):
        bot.send_message(message.chat.id, 'Давай попробуем заново')
        start(message)

    else:
        bot.send_message(message.chat.id, 'Нет такой функции')

def delete_user(user_id):  # FIX IT
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
        cur = con.cursor()

        cur.execute('DELETE FROM users WHERE telegram_id=?', (telegram_id,))

        con.commit()






@bot.message_handler(commands=['search'])
def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1❤️")
    btn2 = types.KeyboardButton("2👎")
    btn3 = types.KeyboardButton("3💤")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text=
    '''
    1.Нравится
    2.Не нравится
    3.Вернутся в главное меню
        ''', reply_markup=markup)

    text = message.text

    if (text == "1"):
        bot.send_message(message.chat.id, 'Давай попробуем заново')

    elif  (text == "2"):
        bot.send_message(message.chat.id, 'Давай попробуем заново')

    elif  (text == "3"):
        bot.send_message(message.chat.id, 'Перенаправляю в главное меню')
        menuFirst(message)

    else:
        bot.send_message(message.chat.id, 'Нет такой функции')







   # cur.execute('INSERT INTO users (name, age) VALUES ("%s","%s")' % (name, age))
   # conn.commit()
   # cur.close()
   # conn.close()




bot.polling(none_stop=True)

