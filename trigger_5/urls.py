from django.urls import path
from . import views

app_name = 'trigger_5'

urlpatterns = [
    path('pageBahanMakanan/', views.pageBahanMakanan, name='BahanMakanan'),
    path('pageTransaksiPemesanan/', views.pageTransaksiPemesanan, name='TransaksiPemesanan'),
    path('pageDetailTransaksiPemesanan/', views.pageDetailTransaksiPemesanan, name='TransaksiPemesanan'),
    path('pageKategoriRestoran/', views.pageKategoriRestoran, name='KategoriRestoran'),
]