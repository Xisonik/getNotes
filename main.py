import telebot
import sqlite3
from get_notes import get_notes
from get_audio import get_audio
from audio_to_midi import audio_to_midi
import uuid
import os
import numpy as np

name = None
names = dict()
bot = telebot.TeleBot('7944304752:AAEGLjXQI9LiySM7F4AkwG4bUSHKtq9Kbu0')

def get_tone_user():
    # Подключение к базе данных
    conn = sqlite3.connect('person.sql')
    c = conn.cursor()
    # Выполнение запроса на выборку значений из таблицы
    c.execute("SELECT tone FROM users WHERE name = '%s'" % name)
    # c.execute("SELECT * FROM users")
    results = c.fetchall()

    # Вывод результатов
    for row in results:
        print(row)

    # Закрытие соединения с базой данных
    conn.close()
    return results[-1][0]

bad_include = ["Ну что, ленивый пирожок, лови свою расшифровку. ",
               "Ну и нахал, ладно, мне не жалко. "]

good_include = ["Ой ты батюшки, пирожочек захотел расшифровку, держи. ",
                "Держи моя булочка. "]

def get_text(rnotes):
    tone = get_tone_user()
    include_id = np.random.randint(2)
    text = ""
    include = ""
    if tone == 'bad':
        include = bad_include[include_id]
    else:
        include = good_include[include_id]
    print("tone = ", tone,)
    for note in rnotes:
        n = note[1]
        if n in (11, 12, 13, 14):
            snn = f' {n} тактов '
        elif n % 10 == 1:
            snn = f' {n} такт '
        elif n % 10 in (2, 3, 4):
            snn = f' {n} такта '
        else:
            snn = f' {n} тактов '
        text += str(note[0]) + snn + ", "
    text = include + "ты спел " + text
    print(text)
    return text

def get_reply(notes):
    reply = ""
    t = 0
    rnotes = []
    current_note = notes[0]
    for note in notes:
        if current_note == note:
            t += 1
        else:
            rnotes.append([current_note, t])
            current_note = note
            t = 1
    rnotes.append([current_note, t])
    print("notes fore reply", rnotes)
    text = get_text(rnotes)
    return text

from telebot import types
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('person.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), tone varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Как тебя величать, герой?')
    bot.register_next_step_handler(message, user_name)
    


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_voice = "voice_messages/" + filename + ".ogg"
    file_name_midi = "midis/" + filename + ".mid"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_voice, 'wb') as new_file:
        new_file.write(downloaded_file)
    audio_to_midi(file_name_voice, file_name_midi)
    notes = get_notes(file_name_midi)
    if notes != []:
        reply = get_reply(notes)
    else:
        reply = "Спойте нормально, ничего не слышно"
    bot.reply_to(message, reply)
    answer = get_audio(reply, filename)
    audio = open(answer, 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()

def user_name(message):
    global name
    name = message.text.strip()
    names[name] = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Уважительно', callback_data='good'))
    markup.add(types.InlineKeyboardButton('Пренебрежительно', callback_data='bad'))
    bot.send_message(message.chat.id, 'Как бы ты хотел, чтобы с тобой общались?', reply_markup=markup)
    bot.send_message(message.chat.id, 'Отправляй музыку голосовым')

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    print("Он выбрал " + callback.data)
    if callback.data == 'good':
        tone = 'good'
    elif callback.data == 'bad':
        tone = 'bad'
    else:
        tone = 'nan'
    conn = sqlite3.connect('person.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, tone) VALUES ('%s', '%s')" % (name, tone))
    conn.commit()
    cur.close()
    conn.close()

bot.polling(non_stop=True) 