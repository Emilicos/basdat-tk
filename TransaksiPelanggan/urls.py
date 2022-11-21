from django.urls import path
from TransaksiPelanggan.views import *

app_name = 'TransaksiPelanggan'

urlpatterns = [
    path('BuatPesanan/', buat_pesanan, name='buat_pesanan'),
    path('PilihResto/', pilih_resto, name='pilih_resto'),
    path('PilihMenu/', pilih_menu, name='pilih_menu'),
    path('DaftarPesanan/', daftar_pesanan, name='daftar_pesanan'),
    path('KonfirmasiPembayaran/', konfirmasi_pembayaran, name='konfirmasi_pembayaran'),
    path('RingkasanPesanan/', ringkasan_pesanan, name='ringkasan_pesanan'),
    path('PesananBerlangsung/', pesanan_berlangsung, name='pesanan_berlangsung'),
]