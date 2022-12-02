import random
import string
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse, response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import datetime

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

# Create your views here.

def show_form_kategori_makanan(request):
    if request.method == 'POST':
        namaKategori = request.POST.get('namaKategori')
        if namaKategori != "":
            length = random.randint(1,20)
            id = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
            messages.info(request, 'Kategori berhasil ditambahkan!')
            return redirect('KategoriMakanan:show_daftar_kategori_makanan')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu!')
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'form_kategori_makanan.html', context)

def show_daftar_kategori_makanan(request):

    with connection.cursor() as cursor:
        context = {
            'user': {'role': 'Admin'}
        }

        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT id, name
            FROM FOOD_CATEGORY;
        """)

        kategori = dictfetchall(cursor)
        context['kategori'] = kategori

        for i in range(len(kategori)):
            context['kategori'][i]['nomor'] = str(i+1)

        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    return render(request, 'daftar_kategori_makanan.html', context)

def hapus_kategori_makanan(request, id):

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM FOOD_CATEGORY
            WHERE id={id};
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    messages.info(request, 'Berhasil menghapus kategori makanan!')
    return redirect('KategoriMakanan:show_daftar_kategori_makanan')
