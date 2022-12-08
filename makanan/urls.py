from django.urls import path
from makanan.views import *

app_name = "makanan"

urlpatterns = [
    path('create/', create_makanan, name = 'create_makanan'),
    path('pengguna/', show_makanan, name = 'show_makanan_pengguna'),
    path('restoran/', show_makanan_restoran, name = 'show_makanan_restoran'),
    path('restoran/delete/', delete_food, name = 'delete_makanan_restoran'),
    path('restoran/update/', update_makanan, name = 'update_makanan_restoran'),
]