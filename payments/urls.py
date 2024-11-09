from django.urls import path

from .views import withdraw_page, deposit_page, CheckPayment, payment_page

urlpatterns = [
    path('withdraw-token', withdraw_page, name='withdraw_page'),

    path('deposit-token', deposit_page, name='deposit_page'),

    path('payment-token', payment_page, name='payment_token'),

    path('get-deposit-info', CheckPayment.as_view(), name="check_payment"),

]
