from django.shortcuts import render

# Create your views here.
def show_makanan_restoran(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }
    return render(request, 'show_makanan_restoran.html', context)

def show_makanan(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }
    return render(request, 'show_makanan.html', context)

def create_makanan(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }

    return render(request, 'create_makanan.html', context)