from django.urls import path
from .views import *

app_name = 'resto_pay'

urlpatterns = [
    path('', resto_pay, name='resto_pay'),
    path('isi-saldo/', resto_pay_isi_saldo, name='resto_pay_isi_saldo'),
    path('tarik-saldo/', resto_pay_tarik_saldo, name='resto_pay_tarik_saldo'),
]