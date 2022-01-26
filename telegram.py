from telebot import TeleBot, types
from youtube_download import download_mp3
from os import remove
from spotdl import download_track, get_playlist


TOKEN = "5070594813:AAFh-HwZzWRl2WxBIg_otH6llhAcZPS8Uj8"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я музыкальный бот 🎸\n Что я умею:\n\n✨Могу найти твой трек✨\n\n🌿Могу найти твой плейлист спотифай🌿\n\nВсе треки беруться с открытого видеохостинга Youtube, иногда могут попадаться не правильные аудиодорожки\n\n Жми на /menu или напиши это для начала')


@bot.message_handler(commands=['menu'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    find_button=types.KeyboardButton("Найти трек по названию спотифай")
    playlist_button = types.KeyboardButton("Найти плейлист спотифай")
    #youtube_button = type  s.KeyboardButton("Найти трек по названию в ютуб")
    markup.add(find_button, playlist_button)#, youtube_button)
    bot.send_message(message.chat.id,'Выберите что вам нужно',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):    
    if message.text == 'Найти трек по названию спотифай':
        msg = bot.send_message(message.chat.id, "Введите имя исполнителя")
        bot.register_next_step_handler(msg, get_spotify_artist)
    elif message.text == 'Найти плейлист спотифай':
        msg = bot.send_message(message.chat.id, "Отправьте ссылку на ваш спотифай плейлист")
        bot.register_next_step_handler(msg, get_spotify_playlist_count)
    elif message.text == 'Найти трек по названию в ютуб':
        msg = bot.send_message(message.chat.id, "Для точного поиска введите имя исполнителя и название")
        bot.register_next_step_handler(msg, download_yt_track)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда \n \n Для вызова клавитуры введите:\n/menu\n\n Возможности бота описаны в:\n\n/help")


def download_yt_track(message):
    if message.text == 'Найти трек по названию' or message.text == "Плейлист спотифай":  
        bot.send_message(message.chat.id, 'Нажмите на кнопку "Найти трек по названию" ещё раз и введите исполнителя и название трека')
    else:
        bot.send_message(message.chat.id, "Идёт скачивание трека - " + str(message.text))
        bot.send_message(message.chat.id, "Пожалуйста подождите")
        track = download_mp3(message.text)
        bot.send_message(message.chat.id, "Найден трек")
        audio= open('./downloaded_music/' + track, 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        

def get_spotify_artist(message):
    artist = message.text
    msg = bot.send_message(message.chat.id, "Введите название трека")
    bot.register_next_step_handler(msg, get_spotify_track, artist)


def get_spotify_track(message, artist):
    artist = artist
    name = message.text
    file_name = download_track(name, artist)
    bot.send_audio(message.chat.id, audio=open('./downloaded_music/' + file_name, "rb"))
    remove('./downloaded_music/'+str(file_name))

def get_spotify_playlist_count(message):
    count = message.text
def get_spotify_playlist_url(message):
    playlist_link = message.text
    bot.send_message(message.chat.id, "Плейлист получен")
    playlist = get_playlist(playlist_link)
    bot.send_message(message.chat.id, "Ожидайте скачивания треков")
    for i in range(len(playlist)):
        name = playlist[i]['name']
        print(name)
        artist = playlist[i]['artist']
        bot.send_message(message.chat.id, 'Найден трек: ' + str(artist) +  ' - ' + str(name)+ '\n\n'+ str(i+1)+ '/' + str(len(playlist))+'\n Идёт скачивание')
        try:
            file_name = download_track(name, artist)
        except:
            bot.send_message(message.chat.id, "Не получается скачать трек")
        bot.send_audio(message.chat.id, audio=open('./downloaded_music/'+ file_name,'rb'))
        

bot.polling(none_stop=True)
