from django.urls import path
from pengiriman_tarif_per_km.views import show_tarif, create_tarif
app_name = "tarif"

urlpatterns = [
    path('create/', create_tarif, name = 'create_tarif'),
    path('', show_tarif, name = 'show_tarif'),
]