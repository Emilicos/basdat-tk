from django.urls import path
from authentication.views import *
app_name = "authentication"

urlpatterns = [
    path('', show_login_register, name = "show_login_register"),
    path('login/', show_login, name = 'show_login'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', show_register, name = 'show_register'),
    path('register/admin/', registrasi_admin, name = 'registrasi_admin'),
    path('register/pelanggan/', registrasi_pelanggan, name = 'registrasi_pelanggan'),
    path('register/restoran/', registrasi_restoran, name = 'registrasi_restoran'),
    path('register/kurir/', registrasi_kurir, name = 'registrasi_kurir'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('detail/<str:role>/<str:email>', detail, name = 'detail'),
    path('dashboard/verification/<str:email>/', verification, name = 'verification')
]
