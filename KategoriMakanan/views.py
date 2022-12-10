import random
import string
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.db_utils import dict_fetch_all
from utils.users import get_user_role

# Create your views here.

@csrf_exempt
def show_form_kategori_makanan(request):

    if request.method == 'POST':
        name = request.POST.get('namaKategori')
        if name != "":
            # generate random id
            length = random.randint(1,20)
            id = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
            # insert new category
            with connection.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                    INSERT INTO FOOD_CATEGORY VALUES ('{id}','{name}');
                """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC")

            messages.info(request, 'Kategori berhasil ditambahkan!')
            print(id)
            return redirect('KategoriMakanan:show_daftar_kategori_makanan')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu!')
    
    context = {
        'user': {'role': f"{get_user_role(request.COOKIES['email'])}"}
    }
    return render(request, 'form_kategori_makanan.html', context)

def show_daftar_kategori_makanan(request):

    with connection.cursor() as cursor:
        context = {
        'user': {'role': f"{get_user_role(request.COOKIES['email'])}"}
        }
        # get all category
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT id, name
            FROM FOOD_CATEGORY;
        """)

        kategori = dict_fetch_all(cursor)
        context['kategori'] = kategori

        # numbering
        for i in range(len(kategori)):
            context['kategori'][i]['nomor'] = str(i+1)

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    return render(request, 'daftar_kategori_makanan.html', context)

def hapus_kategori_makanan(request, id):

    with connection.cursor() as cursor:
        # delete category
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM FOOD_CATEGORY
            WHERE id='{id}';
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    messages.info(request, 'Berhasil menghapus kategori makanan!')
    return redirect('KategoriMakanan:show_daftar_kategori_makanan')
