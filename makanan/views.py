from django.shortcuts import render

# Create your views here.
def show_makanan_restoran(request):
    
    return render(request, 'show_makanan_restoran.html', {})

def show_makanan(request):
    
    return render(request, 'show_makanan.html', {})

def create_makanan(request):
    context = {
        "user": "restoran"
    }
    return render(request, 'create_makanan.html', context)