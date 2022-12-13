from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.utils import timezone
import datetime
from utils.users import *

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
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'restaurant':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        # TODO: tanya ke kakaknya apa Pesanan Selesai dan Pesanan Ditolak termasuk Pesanan Berlangsung
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT ua.FName, ua.LName, t.Email, t.DateTime, ts.Name AS TransactionStatus
                    FROM TRANSACTION t,
                        USER_ACC ua,
                        TRANSACTION_HISTORY th,
                        TRANSACTION_STATUS ts
                    WHERE t.Email=ua.Email
                        AND (t.Email, t.Datetime)=(th.Email, th.Datetime)
                        AND th.TSId=ts.Id
                        AND EXISTS(
                            SELECT *
                            FROM TRANSACTION_FOOD tf
                            WHERE t.Email=tf.Email
                            AND t.Datetime=tf.Datetime
                            AND tf.RName='{restaurant_name}'
                            AND tf.RBranch='{restaurant_branch}'
                        )
                        AND ts.Id=(
                            SELECT MAX(th2.TSId)
                            FROM TRANSACTION_HISTORY th2
                            WHERE th2.Email=t.Email
                            AND th2.Datetime=t.Datetime
                            GROUP BY th2.Email, th2.Datetime
                        )
                    ORDER BY t.Datetime DESC;
                ''')
                transaction_list_temp = dict_fetch_all(cursor)
                for i in range(len(transaction_list_temp)):
                    transaction_list_temp[i]['time'] = transaction_list_temp[i]['datetime'].timestamp()
                    transaction_list_temp[i]['formatteddatetime'] = transaction_list_temp[i]['datetime'].strftime('%Y-%m-%d %H:%M:%S')
                transaction_list = []
                for i in range(len(transaction_list_temp)):
                    if transaction_list_temp[i]['transactionstatus'] != 'Pesanan Selesai':
                        transaction_list.append(transaction_list_temp[i])
                context = {
                    'transaction_list': transaction_list,
                    'user': {
                        'role': get_user_role(email),
                    },
                }
                return render(request, 'transaksi_pesanan_daftar.html', context)
        except Exception as e:
            return HttpResponse(status=404)
    return HttpResponse(status=404)

def transaksi_pesanan_detail(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'restaurant':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        # Get Parameters
        transaction_email = request.GET.get('email', '')
        try:
            time_sec = float(request.GET.get('time', 0))
        except Exception as e:
            return HttpResponse(status=400)
        transaction_datetime = datetime.datetime.fromtimestamp(time_sec).strftime('%Y-%m-%d %H:%M:%S')
        # Get Transaction
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT ua.FName AS FName,
                        ua.LName AS LName,
                        t.Datetime AS Datetime,
                        t.Street AS Street,
                        t.District AS District,
                        t.City AS City,
                        t.Province AS Province,
                        t.TotalFood AS TotalFood,
                        t.TotalDiscount AS TotalDiscount,
                        t.DeliveryFee AS DeliveryFee,
                        t.TotalPrice AS TotalPrice,
                        t.CourierId AS CourierId,
                        pm.Name AS PaymentMethod,
                        ps.Name AS PaymentStatus,
                        ts.Name AS TransactionStatus
                    FROM TRANSACTION t,
                        USER_ACC ua,
                        PAYMENT_METHOD pm,
                        PAYMENT_STATUS ps,
                        TRANSACTION_STATUS ts,
                        TRANSACTION_HISTORY th
                    WHERE t.Email='{transaction_email}'
                        AND t.Datetime='{transaction_datetime}'
                        AND t.Email=ua.Email
                        AND (t.Email, t.Datetime)=(th.Email, th.Datetime)
                        AND th.TSId=ts.Id
                        AND t.PMId=pm.Id
                        AND t.PSId=ps.Id
                        AND EXISTS (
                            SELECT *
                            FROM TRANSACTION_FOOD tf
                            WHERE tf.Email=t.Email
                                AND tf.Datetime=t.Datetime
                                AND tf.RName='{restaurant_name}'
                                AND tf.RBranch='{restaurant_branch}'
                        );
                ''')
                transaction_list = dict_fetch_all(cursor)
                if len(transaction_list) == 0:
                    raise Exception('Transaction not found')
                transaction = transaction_list[0]
                transaction['formatteddatetime'] = transaction['datetime'].strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return HttpResponse(status=404)
        # Get Restaurant
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT RName,
                        RBranch,
                        Street,
                        District,
                        City,
                        Province
                    FROM RESTAURANT
                    WHERE RName='{restaurant_name}'
                        AND RBranch='{restaurant_branch}';
                ''')
                restaurant_list = dict_fetch_all(cursor)
                if len(restaurant_list) == 0:
                    raise Exception('Restaurant not found')
                restaurant = restaurant_list[0]
        except Exception as e:
            return HttpResponse(status=404)
        # Get Food
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT FoodName, Amount, Note
                    FROM TRANSACTION_FOOD tf
                    WHERE tf.Email='{transaction_email}'
                        AND tf.Datetime='{transaction_datetime}'
                        AND tf.RName='{restaurant_name}'
                        AND tf.RBranch='{restaurant_branch}';
                ''')
                food_list = dict_fetch_all(cursor)
                for i in range(len(food_list)):
                    if food_list[i]['note'] is None:
                        food_list[i]['note'] = ''
        except Exception as e:
            return HttpResponse(status=404)
        # Get Courier
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT ua.FName AS FName,
                        ua.LName AS LName,
                        c.PlateNum AS PlateNum,
                        c.VehicleType AS VehicleType,
                        c.VehicleBrand AS VehicleBrand
                    FROM USER_ACC ua, COURIER c
                    WHERE ua.Email='{transaction['courierid']}'
                        AND c.Email=ua.Email
                ''')
                courier_list = dict_fetch_all(cursor)
                if len(courier_list) == 0:
                    courier = {
                        'name': '-',
                        'platenum': '-',
                        'vehicletype': '-',
                        'vehiclebrand': '-',
                    }
                else:
                    courier = courier_list[0]
                    courier['name'] = courier['fname'] + ' ' + courier['lname']
        except Exception as e:
            return HttpResponse(status=404)
        context = {
            'transaction': transaction,
            'restaurant': restaurant,
            'food_list': food_list,
            'courier': courier,
            'user': {
                'role': get_user_role(email),
            },
        }
        return render(request, 'transaksi_pesanan_detail.html', context)
    elif request.method == 'PUT':
        put = QueryDict(request.body)
        transaction_email = put.get('email', '')
        try:
            time_sec = float(put.get('time', 0))
        except Exception as e:
            return HttpResponse(status=400)
        transaction_datetime = datetime.datetime.fromtimestamp(time_sec).strftime('%Y-%m-%d %H:%M:%S')
        history_datetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT ts.Id, ts.Name
                    FROM TRANSACTION t, TRANSACTION_HISTORY th, TRANSACTION_STATUS ts
                    WHERE (t.Email,t.Datetime)=(th.Email,th.Datetime)
                        AND th.TSId=ts.Id
                        AND t.Email='{transaction_email}'
                        AND t.Datetime='{transaction_datetime}'
                        AND EXISTS (
                            SELECT *
                            FROM TRANSACTION_FOOD tf
                            WHERE tf.Email=t.Email
                                AND tf.Datetime=t.Datetime
                                AND tf.RName='{restaurant_name}'
                                AND tf.RBranch='{restaurant_branch}'
                        )
                        AND ts.Id=(
                            SELECT MAX(th2.TSId)
                            FROM TRANSACTION_HISTORY th2
                            WHERE (th2.Email,th2.Datetime)=(t.Email,t.Datetime)
                            GROUP BY th2.Email, th2.Datetime
                        );
                ''')
                transaction_history_list = dict_fetch_all(cursor)
                if len(transaction_history_list) == 0:
                    raise Exception('Transaction History Not Found')
                transaction_history = transaction_history_list[0]
        except Exception as e:
            return HttpResponse(status=404)
        last_ts_id = transaction_history['id']
        if last_ts_id == 'TS1' or last_ts_id == 'TS2':
            if last_ts_id == 'TS1':
                new_ts_id = 'TS2'
            elif last_ts_id == 'TS2':
                new_ts_id = 'TS3'
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SET SEARCH_PATH TO SIREST;')
                    cursor.execute(f'''
                        INSERT INTO TRANSACTION_HISTORY VALUES
                        ('{transaction_email}', '{transaction_datetime}', '{new_ts_id}', '{history_datetime}');
                    ''')
                return HttpResponse(status=201)
            except Exception as e:
                return HttpResponse(status=400)
    return HttpResponse(status=404)