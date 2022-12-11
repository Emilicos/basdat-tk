from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json

from utils.db_utils import dict_fetch_all
from utils.users import get_user_role

# Home
def show_login_register(request):
    return render(request, 'login_register.html', {})

# Login
def show_login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    elif request.method == 'POST':
        response = HttpResponse()
        email = request.POST['email']
        password = request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute('SET SEARCH_PATH TO SIREST;')
            cursor.execute(f'''
                SELECT *
                FROM USER_ACC
                WHERE Email='{email}' AND Password='{password}';
            ''')
            user_list = dict_fetch_all(cursor)
        if len(user_list) != 0: # User found
            response.set_cookie('email', email)
            response.set_cookie('password', password)
            response.status_code = 200
            return response
        else: # User not found
            response.delete_cookie('email')
            response.delete_cookie('password')
            response.status_code = 404
            return response
    return HttpResponse(status=404)

# Logout
def logout_user(request):
    response = HttpResponse(status=200)
    response.delete_cookie('email')
    response.delete_cookie('password')
    return redirect('authentication:show_login_register')

# Create your views here.
def show_register(request):
    return render(request, 'register.html', {})

def registrasi_admin(request):
    return render(request, 'registrasi_admin.html', {})

def registrasi_pelanggan(request):
    return render(request, 'registrasi_pelanggan.html', {})

def registrasi_restoran(request):
    return render(request, 'registrasi_restoran.html', {})

def registrasi_kurir(request):
    return render(request, 'registrasi_kurir.html', {})

def dashboard(request):
    email = request.COOKIES['email']
    role = get_user_role(email)
    context = {
        'user': {
            'role': f'{role}',
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")

        if role == 'Admin':
            cursor.execute(f"""
                SELECT * 
                FROM USER_ACC
                WHERE email='{email}';
            """)

            data = dict_fetch_all(cursor)
            data = data[0]
            context['data'] = data

            cursor.execute(f"""
                SELECT * 
                FROM TRANSACTION_ACTOR NATURAL JOIN USER_ACC;
            """)

            t_actor = dict_fetch_all(cursor)
            for i in range(len(t_actor)):
                t_actor[i]['role'] = get_user_role(t_actor[i]['email'])
                if t_actor[i]['adminid'] != None:
                    t_actor[i]['status'] = 'Terverifikasi'
                else:
                    t_actor[i]['status'] = 'Belum Terverifikasi'

            context['t_actor'] = t_actor

            return render(request, 'dashboard_admin.html', context)

        elif role == 'Pelanggan':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * FROM CUSTOMER
                    WHERE email='{email}') C) UC
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0
            
            context['data'] = data
            return render(request, 'dashboard_pelanggan.html', context)

        elif role == 'Kurir':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * FROM COURIER
                    WHERE email='{email}') C) UC
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0
            
            context['data'] = data
            return render(request, 'dashboard_kurir.html', context)

        elif role == 'Restoran':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * 
                    FROM RESTAURANT R JOIN RESTAURANT_CATEGORY RC
                    ON R.rcategory=RC.id
                    WHERE R.email='{email}') R) UR
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0

            if data['rating'] == None:
                data['rating'] = 0
            
            context['data'] = data

            cursor.execute(f"""
                SELECT * FROM RESTAURANT_OPERATING_HOURS
                WHERE name='{data['rname'].replace("'", "''")}' AND branch='{data['rbranch']}';
            """)
            jadwal = dict_fetch_all(cursor)
            context['jadwal'] = jadwal

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")
            return render(request, 'dashboard_restoran.html', context)

def detail(request, role, email):
    context = {
        'user': {
            'role': 'Admin',
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")

        if role == 'Pelanggan':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * FROM CUSTOMER
                    WHERE email='{email}') C) UC
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0
            
            context['data'] = data
            return render(request, 'dashboard_pelanggan.html', context)

        elif role == 'Kurir':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * FROM COURIER
                    WHERE email='{email}') C) UC
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0
            
            context['data'] = data
            return render(request, 'dashboard_kurir.html', context)

        elif role == 'Restoran':
            cursor.execute(f"""
                SELECT * 
                FROM ((SELECT * FROM USER_ACC
                    WHERE email='{email}') U
                    NATURAL JOIN
                    (SELECT * 
                    FROM RESTAURANT R JOIN RESTAURANT_CATEGORY RC
                    ON R.rcategory=RC.id
                    WHERE R.email='{email}') R) UR
                    NATURAL JOIN
                    (SELECT * FROM TRANSACTION_ACTOR
                    WHERE email='{email}') T;
            """)

            data = dict_fetch_all(cursor)
            data = data[0]

            if data['adminid'] != None:
                data['status'] = 'Terverifikasi'
            else:
                data['status'] = 'Belum Terverifikasi'

            if data['restopay'] == None:
                data['restopay'] = 0
            
            if data['rating'] == None:
                data['rating'] = 0
                
            context['data'] = data

            cursor.execute(f"""
                SELECT * FROM RESTAURANT_OPERATING_HOURS
                WHERE name='{data['rname'].replace("'", "''")}' AND branch='{data['rbranch']}';
            """)
            jadwal = dict_fetch_all(cursor)
            context['jadwal'] = jadwal

            cursor.execute(f"""
                SELECT P.promoname as promoname 
                FROM (SELECT *
                    FROM RESTAURANT_PROMO
                    WHERE rname='{data['rname'].replace("'", "''")}' AND rbranch='{data['rbranch']}'
                    AND RPromo_start <= CURRENT_DATE AND RPromo_end >= CURRENT_DATE) RP 
                    JOIN PROMO P
                ON RP.pid=P.id;
            """)
            promo = dict_fetch_all(cursor)
            context['promo'] = promo

            cursor.execute("SET SEARCH_PATH TO PUBLIC;")
            return render(request, 'dashboard_restoran.html', context)

def verification(request, email):
    role = get_user_role(request.COOKIES['email'])
    if role == 'Admin':
        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE TRANSACTION_ACTOR
                SET AdminId='{request.COOKIES['email']}'
                WHERE Email='{email}';
            """)
    return HttpResponse()

def detail_restoran(request):
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'dashboard_restoran.html', context)

def detail_kurir(request):
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'dashboard_kurir.html', context)

from django.core import serializers
def all_user(request):
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO SIREST;')
        cursor.execute(f'''
            SELECT *
            FROM USER_ACC;
        ''')
    user_list = dict_fetch_all(cursor)
    return HttpResponse(serializers.serialize("json", user_list), content_type="application/json")


