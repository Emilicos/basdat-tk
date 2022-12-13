from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.db_utils import dict_fetch_all
from utils.users import get_user_role
import random
import string

# Create your views here.

@csrf_exempt
def show_form_kategori_restoran(request):

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
                    INSERT INTO RESTAURANT_CATEGORY VALUES ('{id}','{name}');
                """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC")

            messages.info(request, 'Kategori berhasil ditambahkan!')
            print(id)
            return redirect('kategori_restoran:show_daftar_kategori_restoran')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu!')
    
    context = {
        'user': {'role': f"{get_user_role(request.COOKIES['email'])}"}
    }
    return render(request, 'form_kategori_restoran.html', context)

def show_daftar_kategori_restoran(request):

    with connection.cursor() as cursor:
        context = {
        'user': {'role': f"{get_user_role(request.COOKIES['email'])}"}
        }
        # get all category
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT RC.id as id, RC.name as name, R.RCategory as RCategory
            FROM RESTAURANT_CATEGORY RC LEFT OUTER JOIN 
                (SELECT DISTINCT RCategory
                FROM RESTAURANT) R
            ON RC.Id=R.RCategory;
        """)

        kategori = dict_fetch_all(cursor)
        context['kategori'] = kategori
        

        # numbering
        for i in range(len(kategori)):
            context['kategori'][i]['nomor'] = str(i+1)
            if (context['kategori'][i]['rcategory'] != None):
                context['kategori'][i]['status'] = 0
            else:
                context['kategori'][i]['status'] = 1

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    return render(request, 'kategori_restoran.html', context)

def hapus_kategori_restoran(request, id):

    with connection.cursor() as cursor:
        # delete category
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM RESTAURANT_CATEGORY
            WHERE id='{id}';
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    messages.info(request, 'Berhasil menghapus kategori restoran!')
    return redirect('kategori_restoran:show_daftar_kategori_restoran')
