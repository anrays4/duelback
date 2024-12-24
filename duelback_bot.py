import telebot
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

API_TOKEN = '8041774615:AAFSOfK19ZX6D5Stz80uWd5tXYSK0PRge60'

bot = telebot.TeleBot(API_TOKEN)

main_url = "https://www.duelback.com"
mini_app_url = "https://www.duelback.com/register"
sign_up_url = 'https://www.duelback.com/register/player'
group_name = "duelbackgame"


def create_join_to_channel_btn():
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("Join Channel 🔗", url=f"https://t.me/{group_name}")
    check_button = InlineKeyboardButton("Check status ✅", callback_data="check_membership")
    keyboard.add(join_button)
    keyboard.add(check_button)
    return keyboard


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
    response = requests.request("POST", sign_up_url, data=payload)

    is_member = bot.get_chat_member(chat_id="@duelbackgame", user_id=user_id)
    if is_member.status != "left":
        keyboard = InlineKeyboardMarkup()
        web_app_info = WebAppInfo(mini_app_url)

        play_button = InlineKeyboardButton(text="🎮 Play 💰", web_app=web_app_info)
        keyboard.add(play_button)

        with open(f'logo.jpg', 'rb') as photo:

            caption_text = "*** \n Welcome to the Duelback Betting Platform. We are committed to providing a secure, fair, " \
                           f"and transparent environment for all users. \n\n User ID :{user_id} \n Login with link :\n" \
                           f" {main_url} \n Or you can play on MiniApp 👇👇👇👇"

            bot.send_photo(message.chat.id, photo, caption=caption_text, reply_markup=keyboard)
    else:
        join_channel_keyboard = create_join_to_channel_btn()
        bot.send_message(message.chat.id, "Welcome! Please join to our group 👇:", reply_markup=join_channel_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if call.data == "check_membership":
        is_member = bot.get_chat_member(chat_id="@duelbackgame", user_id=user_id)
        if is_member.status != "left":
            keyboard = InlineKeyboardMarkup()
            web_app_info = WebAppInfo(mini_app_url)

            play_button = InlineKeyboardButton(text="🎮 Play 💰", web_app=web_app_info)
            keyboard.add(play_button)

            with open(f'logo.jpg', 'rb') as photo:

                caption_text = "*** \n Welcome to the Duelback Betting Platform. We are committed to providing a secure, fair, " \
                               f"and transparent environment for all users. \n\n User ID :{user_id} \n Login with link :\n" \
                               f" {main_url} \n Or you can play on MiniApp 👇👇👇👇"

                bot.send_photo(user_id, photo, caption=caption_text, reply_markup=keyboard)
        else:
            join_channel_keyboard = create_join_to_channel_btn()
            bot.send_message(user_id, "Welcome! Please join to our group 👇:", reply_markup=join_channel_keyboard)


bot.polling()
