from django.shortcuts import render

DUMMY_LIST = [
    {
        'cabang-restoran': 'Warung EM JE',
        'nama-pelanggan': 'EM JE',
        'waktu-pesanan-dibuat': '2022/10/12\n14:45:00',
        'status-pesanan': True,        
    },
    {
        'cabang-restoran': 'Warung Kelas 2',
        'nama-pelanggan': 'Saiberpang',
        'waktu-pesanan-dibuat': '2077/10/12\n25:00:00',
        'status-pesanan': True,
    },
    {
        'cabang-restoran': 'Metro Rakyat',
        'nama-pelanggan': 'Arteem',
        'waktu-pesanan-dibuat': '2033/10/12\n13:37:00',
        'status-pesanan': True,
    },
]

# Create your views here.

def transaksi_pesanan_detail(request, id): # TODO instead pake dummy, coba fetch dari db list kurir
    context = {
        'dummy': DUMMY_LIST[id - 1],
        'user': {
            'role': 'Kurir',
        },
    }
    return render(request, 'transaksi_pesanan_detail.html', context)

#TODO bikin views yang render halaman sehabis klik details & selesai buat html transaksi_pesanan_kurir.html
def pesanan_detail(request)
    return render(request, 'detail_transaksi_pemesanan_kurir.html')