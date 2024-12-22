import telebot
import sqlite3
from get_notes import get_notes
from get_audio import get_audio
from audio_to_midi import audio_to_midi
import uuid
import os


bot = telebot.TeleBot('7944304752:AAEGLjXQI9LiySM7F4AkwG4bUSHKtq9Kbu0')

def user_tone(message):
    tone = message.text.strip()
    
    conn = sqlite3.connect('person.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name) VALUES ('%s')" % (tone))
    conn.commit()
    cur.close()
    conn.close()

def get_text(rnotes):
    text = "вы использовали "
    
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
        text += str(note[0]) + snn
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


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('person.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, tone varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    get_notes("audio/test.mid")
    bot.send_message(message.chat.id, 'Как бы ты хотел, чтобы с тобой общались?')
    bot.register_next_step_handler(message, user_tone)


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



bot.polling(non_stop=True)