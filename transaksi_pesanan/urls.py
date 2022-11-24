from django.urls import path
from .views import *

app_name = 'transaksi_pesanan'

urlpatterns = [
    path('', transaksi_pesanan_daftar, name='transaksi_pesanan_daftar'),
    path('detail/<int:id>/', transaksi_pesanan_detail, name='transaksi_pesanan_detail'),
]