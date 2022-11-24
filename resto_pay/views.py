from django.shortcuts import render

# Create your views here.
def resto_pay(request):
    context = {
        'saldo': 10000,
        'user': {
            'role': 'Pelanggan'
        },
    }
    return render(request, 'resto_pay.html', context)

def resto_pay_isi_saldo(request):
    context = {
        'saldo': 10000,
        'bank_nama': 'Bank Sendiri',
        'bank_norek': '50122352',
        'user': {
            'role': 'Pelanggan'
        },
    }
    return render(request, 'resto_pay_isi_saldo.html', context)

def resto_pay_tarik_saldo(request):
    context = {
        'saldo': 10000,
        'bank_nama': 'Bank Sendiri',
        'bank_norek': '50122352',
        'user': {
            'role': 'Pelanggan'
        },
    }
    return render(request, 'resto_pay_tarik_saldo.html', context)