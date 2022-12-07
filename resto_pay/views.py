from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse

from utils.db_utils import dict_fetch_all
from utils.users import *

# Create your views here.
def resto_pay(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO SIREST;')
        cursor.execute(f'''
            SELECT RestoPay
            FROM TRANSACTION_ACTOR
            WHERE Email='{email}';
        ''')
        resto_pay_list = dict_fetch_all(cursor)
    if len(resto_pay_list) != 0:
        context = {
            'saldo': resto_pay_list[0]['restopay'],
            'user': {
                'role': get_user_role(email),
            },
        }
        return render(request, 'resto_pay.html', context)
    return HttpResponse(status=404)

def resto_pay_isi_saldo(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SET SEARCH_PATH TO SIREST;')
            cursor.execute(f'''
                SELECT RestoPay, BankName, AccountNo
                FROM TRANSACTION_ACTOR
                WHERE Email='{email}';
            ''')
            resto_pay_list = dict_fetch_all(cursor)
        if len(resto_pay_list) != 0:
            context = {
                'saldo': resto_pay_list[0]['restopay'],
                'bank_nama': resto_pay_list[0]['bankname'],
                'bank_norek': resto_pay_list[0]['accountno'],
                'user': {
                    'role': get_user_role(email),
                },
            }
            return render(request, 'resto_pay_isi_saldo.html', context)
    elif request.method == 'POST':
        perubahan_saldo = int(request.POST.get('nominal', 0))
        # IMPORTANT! sesuai soal, yang dihandle oleh trigger BUKAN PENGISIAN saldo tetapi PENARIKAN saldo
        # Jadi untuk yang ini dihandle oleh saya karena PENGISIAN
        if perubahan_saldo >= 0:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SET SEARCH_PATH TO SIREST;')
                    cursor.execute(f'''
                        UPDATE TRANSACTION_ACTOR
                        SET RestoPay = RestoPay + {perubahan_saldo}
                        WHERE Email='{email}';
                    ''')
                return JsonResponse({
                    'message': 'Success',
                }, status=201)
            except Exception as e:
                res = str(e).split('\n')[0]
                return JsonResponse({
                    'message': res,
                }, status=400)
        else:
            return JsonResponse({
                'message': 'Nominal harus bernilai non-negatif',
            }, status=400)
    return HttpResponse(status=404)

def resto_pay_tarik_saldo(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SET SEARCH_PATH TO SIREST;')
            cursor.execute(f'''
                SELECT RestoPay, BankName, AccountNo
                FROM TRANSACTION_ACTOR
                WHERE Email='{email}';
            ''')
            resto_pay_list = dict_fetch_all(cursor)
        if len(resto_pay_list) != 0:
            context = {
                'saldo': resto_pay_list[0]['restopay'],
                'bank_nama': resto_pay_list[0]['bankname'],
                'bank_norek': resto_pay_list[0]['accountno'],
                'user': {
                    'role': get_user_role(email),
                },
            }
            return render(request, 'resto_pay_tarik_saldo.html', context)
    elif request.method == 'POST':
        perubahan_saldo = int(request.POST.get('nominal', 0))
        # Penarikan saldo negatif akan dihandle oleh Trigger!!
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    UPDATE TRANSACTION_ACTOR
                    SET RestoPay = RestoPay - {perubahan_saldo}
                    WHERE Email='{email}';
                ''')
            return JsonResponse({
                'message': 'Success',
            }, status=201)
        except Exception as e:
            res = str(e).split('\n')[0]
            return JsonResponse({
                'message': res,
            }, status=400)
    return HttpResponse(status=404)