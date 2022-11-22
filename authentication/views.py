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
