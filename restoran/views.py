from django.shortcuts import render

# Create your views here.
def show_detail_restoran(request):
    context = {
        "user": {
            'role': 'Pelanggan'
        }
    }
    return render(request, 'detail_restoran.html', context)

def show_daftar_restoran(request):
    context = {
        "user": {
            'role': 'Pelanggan'
        }
    }
    return render(request, 'daftar_restoran.html', context)
