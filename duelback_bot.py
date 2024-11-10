import telebot
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

API_TOKEN = '8041774615:AAFSOfK19ZX6D5Stz80uWd5tXYSK0PRge60'

bot = telebot.TeleBot(API_TOKEN)

mini_app_url = "https://www.duelback.com/register"
sign_up_url = 'https://www.duelback.com/register/player'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    referral = message.text.split()[-1]
    username = message.from_user.username

    user_id = message.from_user.id
    file_url = ""
    try:
        photos = bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id

            file_info = bot.get_file(file_id)

            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    except:
        pass

    payload = {
        'user_id': user_id,
        'username': username,
        'ref_code': referral,
        'avatar': file_url,
    }
    print(referral)
    response = requests.request("POST", sign_up_url, data=payload)

    keyboard = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(mini_app_url)

    play_button = InlineKeyboardButton(text="Play 🎮💰", web_app=web_app_info)
    keyboard.add(play_button)

    with open(f'logo.jpg', 'rb') as photo:

      caption_text = "*** \n Welcome to the Duelback Betting Platform. We are committed to providing a secure, fair, and transparent environment for all users."

      bot.send_photo(message.chat.id, photo, caption=caption_text, reply_markup=keyboard)


bot.polling()