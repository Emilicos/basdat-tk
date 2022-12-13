import datetime
from distutils.command.clean import clean
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime
import random
import string
from django.views.decorators.csrf import csrf_exempt


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

@csrf_exempt
def show_form_bahan_makanan(request):
    if request.method == 'POST':
        namaBahan = request.POST.get('namaBahan')
        print(namaBahan)
        id = "i" + f"{random.randint(1, 1000000)}"
        with connection.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                INSERT INTO INGREDIENT VALUES
                ('{id}', '{namaBahan}');
                 """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        return JsonResponse({
                    "message": "Successful"
                })
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
            SELECT *
            FROM INGREDIENT;
        """)

        bahan = dictfetchall(cursor)
        context['bahan'] = bahan


        cursor.execute("SET SEARCH_PATH TO PUBLIC")
        for item in bahan :
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                        SELECT *
                        FROM FOOD_INGREDIENT
                        WHERE INGREDIENT = '{item['id']}';
                    """)
                transaction_food_data = dictfetchall(cursor)
                if(len(transaction_food_data) > 0):
                    item['referred'] = True
                else:
                    item['referred'] = False


    return render(request, 'bahan_makanan.html', context)

def hapus_bahan_makanan(request, id): # TODO syntax delete makanan dengan if variable di branch FOOD_INGREDIENT dia equals / viable dengan yg ada di FOOD db
#kalo udah di refer sama makanan baru gabisa dihapus
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM INGREDIENT
            WHERE id='{id}';
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    messages.info(request, 'Berhasil menghapus bahan makanan!')
    return redirect('bahan_makanan:show_form_daftar_makanan')