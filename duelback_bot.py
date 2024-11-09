import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6877055485:AAFsii5hGHW9kXvsrd8zsphwa2P6IXcmg7s'

bot = telebot.TeleBot(API_TOKEN)

mini_app_url = "https://google.com/"
sign_up_url = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    referral = message.text.split()[-1]
    user_id = message.chat.id
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

    print(file_url)
    payload = {
        'user_id': user_id,
        'username': username,
        'referral': referral,
        'avatar': file_url,
    }

    response = requests.request("POST", sign_up_url, data=payload)

    print(response.text)

    # ساخت دکمه شیشه‌ای (inline button) با URL
    keyboard = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(mini_app_url)  # URL مربوط به مینی‌اپ شما

    # ایجاد دکمه شیشه‌ای با WebAppInfo
    play_button = InlineKeyboardButton(text="Play", web_app=web_app_info)
    keyboard.add(play_button)

    caption_text = "به بازی خوش آمدید! روی دکمه زیر کلیک کنید تا بازی کنید."

    bot.send_message(chat_id=message.chat.id, text=caption_text, reply_markup=keyboard)


bot.polling()