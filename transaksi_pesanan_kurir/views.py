from django.shortcuts import render
from django.db import connection
from utils.db_utils import dict_fetch_all
import json

# Create your views here.

def transaksi_pesanan_detail(request): # TODO instead pake dummy, coba fetch dari db list kurir
    
    context = {
        'user': {
            'role': 'Kurir',
        },
    }

    context['rname'] = request.GET.get("rname").strip()
    context['rbranch'] = request.GET.get("rbranch").strip()
    context['nama_pelanggan'] = request.GET.get("nama_pelanggan").strip()

    context['waktu_pemesanan'] = request.GET.get("waktu_pemesanan").strip()
    context['jalan'] = request.GET.get("jalan")
    
    context['kecamatan'] = request.GET.get("kecamatan")
    context['kota'] = request.GET.get("kota")
    context['provinsi'] = request.GET.get("provinsi")
    context['total_makanan'] = request.GET.get("total_makanan").strip()
    context['total_diskon'] = request.GET.get("total_diskon").strip()
    context['total_pengantaran'] = request.GET.get("total_pengantaran").strip()
    context['total_harga'] = request.GET.get("total_harga").strip()

    context['payment_method'] = request.GET.get("payment_method").strip()
    context['payment_status'] = request.GET.get("payment_status").strip()

    context['nama_kurir'] = request.GET.get("nama_kurir").strip()
    context['platnomor'] = request.GET.get("platnomor").strip()
    context['jenis_kendaraan'] = request.GET.get("jenis_kendaraan").strip()
    context['merk_kendaraan'] = request.GET.get("merk_kendaraan").strip()

    context['jalan_resto'] = request.GET.get("jalan_resto").strip()
    context['district_resto'] = request.GET.get("district_resto").strip()
    context['city_resto'] = request.GET.get("city_resto").strip()
    context['province_resto'] = request.GET.get("province_resto").strip()

    return render(request, 'detail_transaksi_pemesanan_kurir.html', context)

def transaksi_pesanan_all(request):
    context = {
        'user': {
            'role': 'Kurir'
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM TRANSACTION_FOOD;
                """)
        transaction_food = dict_fetch_all(cursor)
        for item in transaction_food:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT *
                    FROM TRANSACTION
                    WHERE email = '{item['email']}' AND datetime = '{item['datetime']}';
                """)
            transaction_data = dict_fetch_all(cursor)
            item['jalan'] = transaction_data[0]['street']
            item['kecamatan'] = transaction_data[0]['district']
            item['kota'] = transaction_data[0]['city']
            item['provinsi'] = transaction_data[0]['province']
            item['total_makanan'] = transaction_data[0]['totalfood']
            item['total_diskon'] = transaction_data[0]['totaldiscount']
            item['total_pengantaran'] = transaction_data[0]['deliveryfee']
            item['total_harga'] = transaction_data[0]['totalprice']
            item['pmid'] = transaction_data[0]['pmid']
            item['courierid'] = transaction_data[0]['courierid']
            item['psid'] = transaction_data[0]['psid']

            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT *
                    FROM PAYMENT_METHOD
                    WHERE Id = '{item['pmid']}';
                """)
            payment = dict_fetch_all(cursor)
            item['payment_method'] = payment[0]['name']

            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT *
                    FROM PAYMENT_STATUS
                    WHERE Id = '{item['psid']}';
                """)
            payment_id = dict_fetch_all(cursor)
            item['payment_status'] = payment_id[0]['name']

            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT *
                    FROM COURIER
                    WHERE email = '{item['courierid']}';
                """)
            courier_motor = dict_fetch_all(cursor)
            item['platnomor'] = courier_motor[0]['platenum']
            item['jenis_kendaraan'] = courier_motor[0]['vehicletype']
            item['merk_kendaraan'] = courier_motor[0]['vehiclebrand']

            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT Fname, LName
                    FROM USER_ACC
                    WHERE email = '{item['email']}';
                """)
            user_name = dict_fetch_all(cursor)
            item['email'] = f"{user_name[0]['fname']} {user_name[0]['lname']}"

            item['datetime'] = item['datetime'].strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT FName, LName
                    FROM USER_ACC
                    WHERE email = '{item['courierid']}';
                """)
            user_name_courier = dict_fetch_all(cursor)
            item['nama_kurir'] = f"{user_name_courier[0]['fname']} {user_name_courier[0]['lname']}"

            courier_motor = dict_fetch_all(cursor)

            if(item['rname'] != "Venti's"):
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                        SELECT Street, District, City, Province
                        FROM RESTAURANT
                        WHERE rname = '{item['rname']}' AND rbranch = '{item['rbranch']}';
                    """)
                restaurant_info = dict_fetch_all(cursor)
                item['jalan_resto'] = restaurant_info[0]['street']
                item['district_resto'] = restaurant_info[0]['district']
                item['city_resto'] = restaurant_info[0]['city']
                item['province_resto'] = restaurant_info[0]['province']

        context['transaction_food_no_dump'] = transaction_food


    return render(request, 'transaksi_pesanan_kurir.html', context)