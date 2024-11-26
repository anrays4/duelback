import json
import time
from players.models import User
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework import status
from .models import Withdraw, Deposit
from rest_framework.response import Response
from takhte_nard.settings import WEBSITE_URL, DEPOSIT_KEY, WITHDRAW_WALLET_ADDRESS, WITHDRAW_KEY, WALLET_PRIVATE_KEY
import requests
from payments.transaction import send_tron_for_user, check_wallet
from django.contrib.auth.decorators import login_required


@login_required
def withdraw_page(request):
    player = request.user
    payments_history = Withdraw.objects.filter(user=player)
    my_user = get_object_or_404(User, username=player)

    if Withdraw.objects.filter(user=my_user, status="2").exists():
        payment_time = Withdraw.objects.get(user=my_user, status="2")
        if int(time.time()) - payment_time.time_st_for_expired >= 300:
            withdraw_req_is_exist = False
            payment_time.delete()
        else:
            withdraw_req_is_exist = True
    else:
        withdraw_req_is_exist = False

    wallet_error = False
    token_error = False
    send_error = False
    if request.method == "POST":
        token_amount_user = int(request.POST['token'])
        to_wallet = request.POST['wallet']

        if to_wallet[0] != "T":
            wallet_error = True
        else:
            wallet_error = False

        if 20 <= token_amount_user <= my_user.game_token:
            token_error = False
        else:
            token_error = True

        try:
            wallet_is_exist = check_wallet(to_wallet)
        except:
            wallet_is_exist = False

        if not token_error and not wallet_error and wallet_is_exist and not withdraw_req_is_exist:
            new_withdraw_request = Withdraw.objects.create(user=my_user, amount=token_amount_user, crypto_name="tron",
                                                           amount_game_token=token_amount_user, status="2",
                                                           from_address=WITHDRAW_WALLET_ADDRESS, to_address=to_wallet)

            try:
                response = send_tron_for_user(amount=token_amount_user, receiver_address=to_wallet)
                if response['result']:
                    tx_id = response['txid']
                    new_withdraw_request.tx_id = tx_id
                    new_withdraw_request.status = "3"
                    new_withdraw_request.save()

                    my_user.game_token -= token_amount_user
                    my_user.save()

                else:
                    send_error = True
            except:
                send_error = True

    context = {
        'payments': payments_history,
        "wallet_error": wallet_error,
        "token_error": token_error,
        "send_error": send_error,
    }
    return render(request, 'withdraw_page.html', context)


@login_required
def deposit_page(request):
    player = request.user

    payments_history = Deposit.objects.filter(user=player)

    if Deposit.objects.filter(user=player, status="1").exists():
        payment_time = Deposit.objects.get(user=player, status="1")
        if int(time.time()) - payment_time.time_st_for_expired >= 3600:
            has_payment = False
            payment_time.delete()
        else:
            has_payment = True
    else:
        has_payment = False

    if request.method == "POST":
        token_amount_user = request.POST['token']
        token_network = request.POST['network']

        if not has_payment and float(token_amount_user) >= 10:

            new_payment = Deposit.objects.create(user=player, amount=token_amount_user, crypto_name=token_network,
                                                 amount_game_token=token_amount_user, status="1",
                                                 time_st_for_expired=int(time.time()))
            merchant = DEPOSIT_KEY
            token_amount = token_amount_user
            call_back_url = WEBSITE_URL + "/payments/get-deposit-info"
            if token_network == "tron":
                network = "trc20"  # trc20 or bep20
                token = "trx"  # trc20: trx, usdt || bep20: bnb, usdc
            elif token_network == "growbit":
                network = "bep20"
                token = "grb"
            else:
                return redirect("home_page")
            orderId = str(new_payment.id)  # deposit id in my models for confirm users payment

            url = "https://zedteam.xyz/CryptoPay/"
            payload = json.dumps({
                "merchant": merchant,
                "callbackUrl": call_back_url,
                "amount": int(token_amount),
                "network": network,
                "token": token,
                "orderId": orderId
            })

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                response = requests.request("POST", url=url, headers=headers, data=payload)
                res_status = response.json()['status']
                if res_status:
                    res_to_wallet_address = response.json()['wallet']
                    amount_crypto = response.json()['amount']

                    new_payment.to_address = res_to_wallet_address
                    new_payment.amount = amount_crypto
                    new_payment.save()
                    return redirect("payment_token")
                else:
                    new_payment.delete()
                pass
            except:
                new_payment.delete()

    context = {
        'payments': payments_history,
        "has_payment": has_payment,
    }
    return render(request, 'deposit_page.html', context)


@login_required
def payment_page(request):
    player = request.user
    if not Deposit.objects.filter(user=player, status="1").exists():
        return redirect("deposit_page")

    my_payment = Deposit.objects.get(user=player, status="1")

    context = {
        "my_payment": my_payment,
        "time": 3600 - (int(time.time()) - my_payment.time_st_for_expired)
    }
    return render(request, "payment_page.html", context)


class CheckPayment(APIView):
    def post(self, request):
        try:
            id_payment = request.POST['orderId']
            payment = Deposit.objects.get(id=id_payment, status="1")
            deposit_amount = payment.amount_game_token

            if payment.crypto_name == "growbit":
                payment.user.deposit_token_offer(amount=deposit_amount, offer=10)  # 10 is percent
            else:
                payment.user.deposit_token(amount=deposit_amount)

            payment.status = "3"
            payment.from_address = request.POST["sender"]
            payment.save()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except:
            return Response({"status": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
