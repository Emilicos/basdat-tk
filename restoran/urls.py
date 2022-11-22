from django.urls import path
from restoran.views import *

app_name = "restoran"

urlpatterns = [
    path('detail/', show_detail_restoran, name = 'show_detail_restoran'),
    path('', show_daftar_restoran, name = 'show_daftar_restoran'),
]