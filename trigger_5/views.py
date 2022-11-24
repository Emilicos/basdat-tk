# Create your views here.
import datetime, json
from distutils.command.clean import clean
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def pageBahanMakanan(request):
    context = {
        "user": {
            'role': 'Admin'
        }
    }
    return render(request, 'bahan_makanan.html', context)

def pageKategoriRestoran(request):
    context = {
        "user": {
            'role': 'Admin'
        }
    }
    return render(request, 'forms_kategori_restoran.html', context)

def pageTransaksiPemesanan(request):
    return render(request, 'transaksi_pemesanan.html')