
import telebot
import sqlite3 as sq
from telebot import types

bot = telebot.TeleBot('7155989263:AAFcqabkraoHUo7DnPQsi51Fh0kBPXk6Vrg')
id = None
name = None
age = None
gender = None
search = None
city = None
AboutMe = None
downloaded_file = None




@bot.message_handler(commands=['start'])
def start(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,telegram_id INTEGER, name TEXT, age INTEGER, gender INTEGER,search INTEGER, city TEXT, foto BLOB, AboutMe TEXT )')
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

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, '''Ваш пол?
    1.Мужской
    2.Женский''', reply_markup=markup)


    bot.register_next_step_handler(message, user_search)

def user_search(message):
    global gender
    gender = message.text.strip()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, '''Кого вы хотите искать?
    1.Парня
    2.Девушку
    3.Неважно''', reply_markup=markup)


    bot.register_next_step_handler(message, user_gender)

def user_gender(message):
    global search
    search = message.text.strip()


    bot.send_message(message.chat.id, 'Введите город')
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

    user_FinReg(message)

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
2.НЕТ (заполнить анкету сначала)
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
        search_users(message)

    elif (text == "2"):

        delete_user(telegram_id)

        bot.send_message(message.chat.id, 'Давай попробуем заново')
        start(message)
    elif (text == "3"):
        bot.send_message(message.chat.id, 'Отправь новую фотографию')
        bot.register_next_step_handler(message, new_user_foto)
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

def new_user_foto(message):
    global downloaded_file
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()

    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)

    # Загружаем сам файл
    downloaded_file = bot.download_file(file_info.file_path)

    cur.execute('UPDATE users SET foto = ? WHERE telegram_id = ?', (downloaded_file, telegram_id))
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
                "INSERT INTO users (telegram_id, name, age, gender, search, city, foto, AboutMe ) VALUES (?,?,?,?,?,?,?,?);", (
                telegram_id, name, age, gender, search, city, downloaded_file, AboutMe))
            con.commit()
            menuFirst(message)

    elif (text == "2"):
        bot.send_message(message.chat.id, 'Давай попробуем заново')
        start(message)

    else:
        bot.send_message(message.chat.id, 'Нет такой функции')

def delete_user(user_id):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
        cur = con.cursor()

        cur.execute('DELETE FROM users WHERE telegram_id=?', (telegram_id,))

        con.commit()






@bot.message_handler(commands=['search'])
def search_users(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
        cur = con.cursor()
    global current_index
    current_index = 0

    algorithm(message)


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




    bot.register_next_step_handler(message, algorithm)

@bot.message_handler(content_types=['Algo'])
def algorithm(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
      cur = con.cursor()
      telegram_id = message.from_user.id


    search = cur.execute('SELECT search FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()
    result = str(search[0])



    if (result == '1'):


        id = 16
        cur.execute('SELECT name, age, city, foto FROM users WHERE gender = 1').fetchone()

        name, age, city, foto = cur.fetchone()

        bot.send_photo(message.chat.id, foto)
        bot.send_message(message.chat.id, name + ", " + str(age) + ", " + city)


        bot.register_next_step_handler(message, search_users)

    else:
        bot.send_message(message.chat.id, 'Давай попробуем заново')







      #elif (search == 2):
       # user =  con.execute('SELECT * FROM users WHERE gender = 2').fetchone()
        #  return user
      #else:
       #   con.execute('SELECT * FROM users WHERE gender = 3').fetchone()

  #  if (text == "1"):
    #    bot.send_message(message.chat.id, 'Давайте начнем поиск!')

   # elif (text == "2"):
     #   bot.send_message(message.chat.id, 'Давай попробуем заново')

    #elif (text == "3"):
     #   bot.send_message(message.chat.id, 'Перенаправляю в главное меню')
     #   menuFirst(message)
    #else:
     #   bot.send_message(message.chat.id, 'Нет такой функции')

#def lastUser(message):
   # telegram_id = message.from_user.id
# if(telegram_id == telegram_id)


bot.polling(none_stop=True)

