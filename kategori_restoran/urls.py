from django.urls import path
from kategori_restoran.views import *

app_name = 'kategori_restoran'

urlpatterns = [
    path('form/', show_form_kategori_restoran, name='show_form_kategori_restoran'),
    path('daftar/', show_daftar_kategori_restoran, name='show_daftar_kategori_restoran'),
    path('hapus/<str:id>', hapus_kategori_restoran, name='hapus_kategori_restoran'),
]