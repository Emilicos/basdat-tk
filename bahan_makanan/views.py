import datetime, json
from distutils.command.clean import clean
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
import random
import string

kursor = connection.cursor()

@login_required
def show_daftar_bahan_makanan(request):
    if request.session.get("role") != "admin":
        return HttpResponse("Anda tidak mmemiliki akses ke halaman ini")
    kursor.execute("SELECT * FROM x.ingredient")
    ingredients = kursor.fetchall()
    ingredients_fix = []
    for ingredient in ingredients:
        id = ingredients[0]
        name = ingredients[1]
        kursor.execute("SELECT * FROM x.food_ingredient WHERE ingredient = %s", [id])
        ingredient = {
            "id" : id,
            "name" : name, 
            "is_referenced" : kursor.fetchone() is not None,
        }
        ingredients_fix.append(ingredient)
    return render(
        request, "bahan_makanan.html", {"ingredients" : ingredients_fix}
    )

@login_required
def show_form_bahan_makanan(request):
    if request.session.get("role") != "admin":
        return HttpResponse("Anda tidak memiliki akses ke halaman ini")
    if request.method == "POST":
        name = request.POST.get("name")
        if name is None or name =="":
            messages.error(request, "Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.")
            return render(request, "form_bahan_makanan.html")
        
        kursor.execute("SELECT MAX(CAST(id AS INT)) FROM x.ingredient")
        id = kursor.fetchone()
        if id is None :
            id = "1"
        else:
            id = str(int(id[0]) + 1)
        try:
            kursor.execute("INSERT INTO x.ingredient(id, name) VALUES (%s, %s)",[id, name],
            )
            messages.success(request, "Berhasil menambahkan bahan makanan baru.")
            return redirect("bahan_makanan:show_daftar_bahan_makanan")
        except Exception as e:
            messages.error(request, e)
    return render(request, "form_bahan_makanan.html")

@login_required
def hapus_bahan_makanan(request, id):
    if request.session.get("role") != "admin":
        return HttpResponse("Anda tidak messages akses ke halaman ini")
    if request.method == "POST":
        try:
            kursor.execute("DELETE FROM x.ingredient WHERE id = %s", [id])
            messages.success(request,"Berhasil menghapus bahan makanan")
        except Exception as e:
            messages.errorMessage(request, "Gagal menghapus bahan makanan")
        return redirect("bahan_makanan:show_daftar_bahan_makanan")
    return HttpResponse("Anda tidak messages akses ke halaman")

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

def hapus_bahan_makanan(request): # TODO syntax delete makanan dengan if variable di branch FOOD_INGREDIENT dia equals / viable dengan yg ada di FOOD db
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