from django.shortcuts import render, redirect
from django.urls import reverse

DUMMY_LIST = [
    {
        'id': 1,
        'hari' : 'Senin',
        'jam_buka' : '08:00:00',
        'jam_tutup' : '21:00:00',
    },
    {
        'id': 2,
        'hari' : 'Selasa',
        'jam_buka': '08:30:00',
        'jam_tutup': '22:00:00',
    },
    {
        'id': 3,
        'hari' : 'Rabu',
        'jam_buka': '13:00:00',
        'jam_tutup': '23:00:00',
    },
]

# Create your views here.
def jam_operasional_buat(request):
    context = {
        'user': {
            'role': 'Restoran',
        },
    }
    return render(request, 'jam_operasional_buat.html', context)

def jam_operasional_daftar(request):
    context = {
        'dummy_list': DUMMY_LIST,
        'user': {
            'role': 'Restoran',
        },
    }
    return render(request, 'jam_operasional_daftar.html', context)

def jam_operasional_ubah(request, id):
    context = {
        'dummy': DUMMY_LIST[id - 1],
        'user': {
            'role': 'Restoran',
        },
    }
    return render(request, 'jam_operasional_ubah.html', context)

def jam_operasional_hapus(request, id):
    return redirect(reverse('jam_operasional:jam_operasional_daftar'))