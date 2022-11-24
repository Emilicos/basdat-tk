from django.urls import path
from authentication.views import *
app_name = "authentication"

urlpatterns = [
    path('', show_login_register, name = "show_login_register"),
    path('login/', show_login, name = 'show_login'),
    path('register/', show_register, name = 'show_register'),
    path('register/admin/', registrasi_admin, name = 'registrasi_admin'),
    path('register/pelanggan/', registrasi_pelanggan, name = 'registrasi_pelanggan'),
    path('register/restoran/', registrasi_restoran, name = 'registrasi_restoran'),
    path('register/kurir/', registrasi_kurir, name = 'registrasi_kurir'),
    path('dashboardpelanggan/', dashboard_pelanggan, name = 'dashboard_pelanggan'),
    path('dashboardrestoran/', dashboard_restoran, name = 'dashboard_restoran'),
    path('dashboardkurir/', dashboard_kurir, name = 'dashboard_kurir'),
    path('dashboardadmin/', dashboard_admin, name = 'dashboard_admin'),
    path('dashboardadmin/pelanggan/', detail_pelanggan, name = 'detail_pelanggan'),
    path('dashboardadmin/kurir/', detail_kurir, name = 'detail_kurir'),
    path('dashboardadmin/restoran/', detail_restoran, name = 'detail_restoran'),
]
