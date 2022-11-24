from django.shortcuts import render

# Create your views here.
def resto_pay(request):
    return render(request, 'resto_pay.html')

def resto_pay_isi_saldo(request):
    return render(request, 'resto_pay_isi_saldo.html')

def resto_pay_tarik_saldo(request):
    return render(request, 'resto_pay_tarik_saldo.html')