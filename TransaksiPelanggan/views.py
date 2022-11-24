from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.

def buat_pesanan(request):
    if request.method == 'POST':
        jalan = request.POST.get('jalan')
        kota = request.POST.get('kota')
        kecamatan = request.POST.get('kecamatan')
        provinsi = request.POST.get('provinsi')
        if jalan != "" and kota != "" and kecamatan != "" and provinsi != "":
            return redirect('TransaksiPelanggan:pilih_resto')
        else:
            messages.info(request, 'Alamat yang diisi belum lengkap!')
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'buat_pesanan.html', context)

def pilih_resto(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'pilih_resto.html', context)

def pilih_menu(request):
    if request.method == 'POST':
        jumlah = int(request.POST.get('menu1')) + int(request.POST.get('menu2')) + int(request.POST.get('menu3')) 
        if jumlah > 0:
            return redirect('TransaksiPelanggan:daftar_pesanan')
        else:
            messages.info(request, 'Belum ada menu yang di pilih!')

    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'pilih_menu.html', context)

def daftar_pesanan(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'daftar_pesanan.html', context)

def konfirmasi_pembayaran(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'konfirmasi_pembayaran.html', context)

def ringkasan_pesanan(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'ringkasan_pesanan.html', context)

def pesanan_berlangsung(request):
    context = {
        'user': {
            'role': 'Pelanggan',
        }
    }
    return render(request, 'pesanan_berlangsung.html', context)
