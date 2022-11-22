from django.urls import path
from KategoriMakanan.views import *

app_name = 'KategoriMakanan'

urlpatterns = [
    path('Form/', show_form_kategori_makanan, name='show_form_kategori_makanan'),
    path('Daftar/', show_daftar_kategori_makanan, name='show_daftar_kategori_makanan'),
    path('Hapus/', hapus_kategori_makanan, name='hapus_kategori_makanan'),
]