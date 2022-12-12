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

def show_daftar_bahan_makanan(request):

    with connection.cursor() as cursor:
        context = {
            'user': {'role': 'Admin'}
        }

        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT rname, rbranch, foodname, ingredient
            FROM FOOD_INGREDIENT;
        """)

        bahan = dictfetchall(cursor)
        context['bahan'] = bahan

        # for i in range(len(kategori)):
        #     context['kategori'][i]['nomor'] = str(i+1)

        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    return render(request, 'bahan_makanan.html', context)

def hapus_bahan_makanan(request):
#kalo udah di refer sama makanan baru gabisa dihapus
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM FOOD_INGREDIENT
            WHERE rname={rname};
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    messages.info(request, 'Berhasil menghapus bahan makanan!')
    return redirect('bahan_makanan:show_daftar_bahan_makanan')