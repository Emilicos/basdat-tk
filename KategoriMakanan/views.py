from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.

def show_form_kategori_makanan(request):
    if request.method == 'POST':
        namaKategori = request.POST.get('namaKategori')
        print(namaKategori)
        if namaKategori != "":
            messages.info(request, 'Kategori berhasil ditambahkan!')
            return redirect('KategoriMakanan:show_daftar_kategori_makanan')
        else:
            messages.info(request, 'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.!')
    return render(request, 'form_kategori_makanan.html')

def show_daftar_kategori_makanan(request):
    return render(request, 'daftar_kategori_makanan.html')
