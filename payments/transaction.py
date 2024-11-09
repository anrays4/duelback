from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from takhte_nard.settings import WITHDRAW_KEY, WALLET_PRIVATE_KEY, WITHDRAW_WALLET_ADDRESS

# Replace 'your_api_key' with the actual API key you obtained from TronGrid
provider = HTTPProvider(api_key=WITHDRAW_KEY)
client = Tron(provider, network='mainnet')

# Sender and receiver addresses
sender_address = WITHDRAW_WALLET_ADDRESS
private_key_hex = WALLET_PRIVATE_KEY


def send_tron_for_user(amount, receiver_address):
    new_amount = amount * 1000000  # Amount in shardi (1 TRX = 1e6 shardi)

    txn = client.trx.transfer(sender_address, receiver_address, new_amount)

    private_key = PrivateKey(bytes.fromhex(private_key_hex))

    signed_txn = txn.build().sign(private_key)

    result = client.broadcast(signed_txn)
    return result


def check_wallet(wallet_address):
    provider_web = HTTPProvider(api_key=WITHDRAW_KEY)
    tron_web = Tron(provider_web, network='mainnet')

    account_info = tron_web.get_account(wallet_address)
    if account_info:
        return True
    else:
        return False
