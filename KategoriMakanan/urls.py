from django.urls import path
from KategoriMakanan.views import *

app_name = 'KategoriMakanan'

urlpatterns = [
    path('FormKategoriMakanan/', show_form_kategori_makanan, name='show_form_kategori_makanan'),
    path('DaftarKategoriMakanan/', show_daftar_kategori_makanan, name='show_daftar_kategori_makanan'),
    path('HapusKategoriMakanan/', hapus_kategori_makanan, name='hapus_kategori_makanan'),
]