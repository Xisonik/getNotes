import telebot

bot = telebot.TeleBot('7944304752:AAEGLjXQI9LiySM7F4AkwG4bUSHKtq9Kbu0')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.id, 'Hi!')

bot.polling(non_stop=True)