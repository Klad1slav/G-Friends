
import telebot
import sqlite3 as sq
from telebot import types

bot = telebot.TeleBot('7155989263:AAFcqabkraoHUo7DnPQsi51Fh0kBPXk6Vrg')
name = None
age = None
gender = None
city = None
foto = None
AboutMe = None


@bot.message_handler(commands=['start'])
def start(message):
    with sq.connect('G!Friends.db', check_same_thread=False) as con:
     cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER primary key, name TEXT, age INTEGER, gender INTEGER, city TEXT, foto BLOB, AboutMe TEXT )')

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
    global foto
    foto = message.text.strip()

    bot.send_message(message.chat.id, 'Расскажите немного про себя')
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

        bot.send_message(message.chat.id, name + ', ' + age + ', '+ city + ', ' + AboutMe)
        bot.send_message(message.chat.id, 'Все верно?')


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('1')
        btn2 = types.KeyboardButton('2')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=
        '''
        1.ДА
        2.НЕТ
        ''', reply_markup=markup)

        if (message.text == "1"):
            with sq.connect('G!Friends.db', check_same_thread=False) as con:
                cur = con.cursor()

                cur.execute(
                    "INSERT INTO users (name, age, gender, city, foto, AboutMe ) VALUES ('%s','%s','%s','%s','%s','%s')" % (name, age, gender, city, foto, AboutMe))
                con.commit()
                menuFirst(message)

        elif (message.text == "2"):
            start(message)




@bot.message_handler(commands=['menu'])
def menuFirst(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text =
    '''
    1.Смотреть анкеты.
    2.Заполнить анкету заново.
    3.Изменить фото/видео.
    4.Изменить текст анкеты.
        ''',reply_markup=markup )

#@bot.message_handler(commands=['user_FinReg_text'])
#def FinRegText(message):



@bot.message_handler(content_types=['menuSec_text'])
def menuSec(message):
   # if (menuSec.message.text == "1"):
     #   bot.register_next_step_handler(search, commands = ['search'])
   # elif (menuSec.message.text == "2"):
      #  bot.register_next_step_handler(message, start)

        bot.send_message(message.chat.id, text="Задай мне вопрос", )



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







   # cur.execute('INSERT INTO users (name, age) VALUES ("%s","%s")' % (name, age))
   # conn.commit()
   # cur.close()
   # conn.close()




bot.polling(none_stop=True)

