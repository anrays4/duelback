import hashlib
import hmac
import json
from urllib.parse import unquote
from takhte_nard.settings import TELEGRAM_BOT_TOKEN

bot_token = TELEGRAM_BOT_TOKEN


# validate mini app init data for check is users of Telegram or not User of Telegram
def validate_init_data(init_data, bot_token=bot_token):
    try:
        decoded_data = {k: unquote(v) for k, v in [pair.split('=') for pair in init_data.split('&')]}
        received_hash = decoded_data.pop('hash', '')
        sorted_data = sorted(decoded_data.items())
        data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted_data])
        secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash == received_hash:
            return True, json.loads(decoded_data.get('user', '{}'))
        else:
            return False, None
    except:
        pass