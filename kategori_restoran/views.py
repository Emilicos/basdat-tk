import datetime, json
from distutils.command.clean import clean
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
import random
import string

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]


def show_form_kategori_restoran(request):
    if request.method == 'POST':
        namaKategori = request.POST.get('namaKategori')
        if namaKategori != "":
            length = random.randint(1,20)
            id = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
            messages.info(request, 'Kategori berhasil ditambahkan!')
            return redirect('KategoriMakanan:show_daftar_kategori_restoran')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.')
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'form_kategori_restoran.html', context)

def show_daftar_kategori_restoran(request):

    with connection.cursor() as cursor:
        context = {
            'user': {'role': 'Admin'}
        }

        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT id, name
            FROM RESTAURANT_CATEGORY;
        """)

        kategori = dictfetchall(cursor)
        context['kategori'] = kategori

        for i in range(len(kategori)):
            context['kategori'][i]['nomor'] = str(i+1)

        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    return render(request, 'kategori_makanan.html', context)

def hapus_kategori_restoran(request, id):

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM RESTAURANT_CATEGORY
            WHERE id={id};
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    messages.info(request, 'Berhasil menghapus kategori restoran!')
    return redirect('KategoriRestoran:show_daftar_kategori_restoran')

def show_form_bahan_makanan(request):
    if request.method == 'POST':
        namaBahan = request.POST.get('namaBahan')
        if namaBahan != "":
            return redirect('KategoriMakanan:show_daftar_bahan_makanan')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.')
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'form_bahan_makanan.html', context)