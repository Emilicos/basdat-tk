from django.shortcuts import render

# Create your views here.
def show_tarif(request):
    
    context = {
        "user": "admin"
    }
    
    return render(request, 'show_tarif.html', context)

def create_tarif(request):
    context = {
        "user": "admin"
    }
    return render(request, 'create_tarif.html', context)