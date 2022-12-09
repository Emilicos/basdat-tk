from django.urls import path
from TransaksiPelanggan.views import *

app_name = 'TransaksiPelanggan'

urlpatterns = [
    path('buatpesanan/', buat_pesanan, name='buat_pesanan'),
    path('pilihresto/', pilih_resto, name='pilih_resto'),
    path('pilihmenu/<str:rname>/<str:rbranch>', pilih_menu, name='pilih_menu'),
    path('daftarpesanan/', daftar_pesanan, name='daftar_pesanan'),
    path('konfirmasipembayaran/', konfirmasi_pembayaran, name='konfirmasi_pembayaran'),
    path('ringkasanpesanan/<str:email>/<str:date_time>', ringkasan_pesanan, name='ringkasan_pesanan'),
    path('pesananberlangsung/', pesanan_berlangsung, name='pesanan_berlangsung'),
    path('bayar/', bayar, name='bayar'),
    path('gagalbayar/', gagal_bayar, name='gagal_bayar'),
]