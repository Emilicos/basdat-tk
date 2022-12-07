from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from utils.db_utils import dict_fetch_all

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
    return response

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

def dashboard_admin(request):
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'dashboard_admin.html', context)

def dashboard_pelanggan(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'dashboard_pelanggan.html', context)

def dashboard_restoran(request):
    context = {
        'user': {
            'role': 'Restoran',
        }
    }
    return render(request, 'dashboard_restoran.html', context)

def dashboard_kurir(request):
    context = {
        'user': {
            'role': 'Kurir',
        }
    }
    return render(request, 'dashboard_kurir.html', context)

def detail_pelanggan(request):
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'dashboard_pelanggan.html', context)

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