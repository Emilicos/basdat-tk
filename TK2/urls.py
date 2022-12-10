"""TK2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, include
import trigger_5.urls as trigger_5


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarif/', include('pengiriman_tarif_per_km.urls')),
    path('makanan/', include('makanan.urls')),
    path('', include('authentication.urls')),
    path('restoran/', include('restoran.urls')),
    path('kategorimakanan/', include('KategoriMakanan.urls')),
    path('transaksipelanggan/', include('TransaksiPelanggan.urls')),
    path('resto-pay/', include('resto_pay.urls')),
    path('jam-operasional/', include('jam_operasional.urls')),
    path('transaksi-pesanan/', include('transaksi_pesanan.urls')),
    # path('', include('trigger_5.urls')),
    path('trigger_5/', include(trigger_5))
]
