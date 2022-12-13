from django.urls import path
from bahan_makanan.views import *

app_name = 'bahan_makanan'

urlpatterns = [
    path('form/', show_form_bahan_makanan, name='show_form_makanan'),
    path('daftar/', show_form_bahan_makanan, name='show_form_bahan_makanan'),
    path('hapus/<str:id>', hapus_bahan_makanan, name='hapus_bahan_makanan'),
]