from django.shortcuts import render

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

def show_login(request):
    return render(request, 'login.html', {})

def show_login_register(request):
    return render(request, 'login_register.html', {})

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