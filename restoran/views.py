from django.shortcuts import render

# Create your views here.
def show_detail_restoran(request):
    return render(request, 'detail_restoran.html', {})

def show_daftar_restoran(request):
    return render(request, 'daftar_restoran.html', {})
