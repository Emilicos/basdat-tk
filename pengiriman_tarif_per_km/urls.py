from django.urls import path
from pengiriman_tarif_per_km.views import show_tarif, show_create_tarif, delete_tarif, update_tarif
app_name = "tarif"

urlpatterns = [
    path('create/', show_create_tarif, name = 'create_tarif'),
    path('delete/<str:id>/', delete_tarif, name = 'delete_tarif'),
    path('', show_tarif, name = 'show_tarif'),
    path('update/', update_tarif, name = 'update_tarif'),
]