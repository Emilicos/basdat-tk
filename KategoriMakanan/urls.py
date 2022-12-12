from django.urls import path
from KategoriMakanan.views import *

app_name = 'KategoriMakanan'

urlpatterns = [
    path('form/', show_form_kategori_makanan, name='show_form_kategori_makanan'),
    path('daftar/', show_daftar_kategori_makanan, name='show_daftar_kategori_makanan'),
    path('hapus/<str:id>', hapus_kategori_makanan, name='hapus_kategori_makanan'),
]