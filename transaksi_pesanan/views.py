from django.shortcuts import render

DUMMY_LIST = [
    {
        'id': 1,
        'nama' : 'Mikayla Putri',
        'jalan': 'Jalan Bahagia nomor 72',
        'kecamatan': 'Cinere',
        'kota': 'Depok',
        'provinsi': 'Jawa Barat',
        'restoran_nama': 'Warung Mantap Depok',
        'restoran_jalan': 'Jalan Sejahtera nomor 5',
        'restoran_kecamatan': 'Bojongsari',
        'restoran_kota': 'Depok',
        'restoran_provinsi': 'Jawa Barat',
        'makanan': [
            'Ayam Goreng (1) - Tidak pakai kulit',
            'Ice Cream (2) - Cair',
        ],
        'makanan_total_harga': 11000,
        'makanan_total_diskon': 0,
        'biaya_pengantaran': 4000,
        'total_biaya': 15000,
        'jenis_pembayaran': 'RestoPay',
        'waktu' : '2022-11-04 11:30:05',
        'status_pembayaran': 'Berhasil',
        'status_pesanan' : 'Menunggu Konfirmasi Restoran',
        'kurir': '-',
        'plat_kendaraan': '-',
        'jenis_kendaraan': '-',
        'merk_kendaraan': '-',
    },
    {
        'id': 2,
        'nama' : 'Kenny Agung',
        'jalan': 'Jalan Bahagia nomor 72',
        'kecamatan': 'Cinere',
        'kota': 'Depok',
        'provinsi': 'Jawa Barat',
        'restoran_nama': 'Warung Mantap Depok',
        'restoran_jalan': 'Jalan Sejahtera nomor 5',
        'restoran_kecamatan': 'Bojongsari',
        'restoran_kota': 'Depok',
        'restoran_provinsi': 'Jawa Barat',
        'makanan': [
            'Ayam Goreng (1) - Tidak pakai kulit',
            'Ice Cream (2) - Cair',
        ],
        'makanan_total_harga': 11000,
        'makanan_total_diskon': 0,
        'biaya_pengantaran': 4000,
        'total_biaya': 15000,
        'jenis_pembayaran': 'RestoPay',
        'waktu' : '2022-11-04 10:54:02',
        'status_pembayaran': 'Berhasil',
        'status_pesanan' : 'Pesanan Dibuat',
        'kurir': '-',
        'plat_kendaraan': '-',
        'jenis_kendaraan': '-',
        'merk_kendaraan': '-',
    },
    {
        'id': 3,
        'nama' : 'Venti Bardbatos',
        'jalan': 'Jalan Bahagia nomor 72',
        'kecamatan': 'Cinere',
        'kota': 'Depok',
        'provinsi': 'Jawa Barat',
        'restoran_nama': 'Warung Mantap Depok',
        'restoran_jalan': 'Jalan Sejahtera nomor 5',
        'restoran_kecamatan': 'Bojongsari',
        'restoran_kota': 'Depok',
        'restoran_provinsi': 'Jawa Barat',
        'makanan': [
            'Ayam Goreng (1) - Tidak pakai kulit',
            'Ice Cream (2) - Cair',
            'Jus Dandelion (1) - Anemo Charged'
        ],
        'makanan_total_harga': 11000,
        'makanan_total_diskon': 0,
        'biaya_pengantaran': 4000,
        'total_biaya': 15000,
        'jenis_pembayaran': 'RestoPay',
        'waktu' : '2022-11-04 10:54:02',
        'status_pembayaran': 'Berhasil',
        'status_pesanan' : 'Pesanan Diantar',
        'kurir': 'Tabibito',
        'plat_kendaraan': 'CEL35T145U5',
        'jenis_kendaraan': 'Motor',
        'merk_kendaraan': 'Shonda',
    },
]

# Create your views here.
def transaksi_pesanan_daftar(request):
    context = {
        'dummy_list': DUMMY_LIST,
    }
    return render(request, 'transaksi_pesanan_daftar.html', context)

def transaksi_pesanan_detail(request, id):
    context = {
        'dummy': DUMMY_LIST[id - 1],
    }
    return render(request, 'transaksi_pesanan_detail.html', context)