import random
import string
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.

def show_form_kategori_makanan(request):
    if request.method == 'POST':
        namaKategori = request.POST.get('namaKategori')
        if namaKategori != "":
            length = random.randint(1,20)
            id = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
            messages.info(request, 'Kategori berhasil ditambahkan!')
            return redirect('KategoriMakanan:show_daftar_kategori_makanan')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu!')
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'form_kategori_makanan.html', context)

def show_daftar_kategori_makanan(request):
    context = {
        'user': {
            'role': 'Admin',
        }
    }
    return render(request, 'daftar_kategori_makanan.html', context)

def hapus_kategori_makanan(request):
    messages.info(request, 'Berhasil menghapus kategori makanan!')
    return redirect('KategoriMakanan:show_daftar_kategori_makanan')
