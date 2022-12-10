from django.urls import path
from . import views

app_name = 'trigger_5'

urlpatterns = [
    path('pageBahanMakanan/', views.pageBahanMakanan, name='BahanMakanan'),
    path('formBahanMakanan/', views.createFormBahanMakanan, name='formBahanMakanan'),
    path('pageTransaksiPemesanan/', views.pageTransaksiPemesanan, name='TransaksiPemesanan'),
    path('pageDetailTransaksiPemesanan/', views.pageDetailTransaksiPemesanan, name='TransaksiPemesanan'),
    path('pageKategoriRestoran/', views.pageKategoriRestoran, name='KategoriRestoran'),
    path('formKategoriRestoran/', views.createFormKategoriRestoran, name='formKategoriRestoran'),
]