from django.urls import path
from . import views

app_name = 'transaksi_pesanan_kurir'

urlpatterns = [
    path('transaksi_pesanan/', views.transaksi_pesanan_all, name='transaksi_pesanan'),
    path('transaksi_pesanan_detail/', views.transaksi_pesanan_detail, name='transaksi_pesanan_detail'),
]