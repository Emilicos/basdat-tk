from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import datetime
from utils.db_utils import dict_fetch_all
from django.views.decorators.csrf import csrf_exempt
from utils.users import get_user_role

class Transaksi:
    def __init__(self):
        self.data = {}
        # {street:str, district:str, city:str, province:str, rname:str, rbranch:str, food:{foodname:[amount, note]}
        # date_time:datetime, p_method:[id, name], id_province:str}

pelanggan = {} # {email:Transaksi()}

# Create your views here.
@csrf_exempt
def buat_pesanan(request):
    email = request.COOKIES['email']

    if request.method == 'POST':
        jalan = request.POST.get('jalan')
        kota = request.POST.get('kota')
        kecamatan = request.POST.get('kecamatan')
        id_provinsi, provinsi = request.POST.get('provinsi').split('_')
        if jalan != "" and kota != "" and kecamatan != "" and provinsi != "":
            pelanggan[email] = Transaksi()
            # store temporary data
            transaksi = pelanggan[email]
            transaksi.data['street'] = jalan
            transaksi.data['city'] = kota
            transaksi.data['district'] = kecamatan
            transaksi.data['id_province'] = id_provinsi
            transaksi.data['province'] = provinsi
            return redirect('TransaksiPelanggan:pilih_resto')
        else:
            messages.info(request, 'Alamat yang diisi belum lengkap!')
    
    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }
    with connection.cursor() as cursor:
        # get province
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT id, province
            FROM DELIVERY_FEE_PER_KM;
        """)

        provinsi = dict_fetch_all(cursor)
        context['provinsi'] = provinsi 

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
    
    return render(request, 'buat_pesanan.html', context)

def pilih_resto(request):
    email = request.COOKIES['email']
    provinsi = pelanggan[email].data['province']

    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }

    with connection.cursor() as cursor:
        # get restaurant
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT RName, RBranch
            FROM RESTAURANT
            WHERE province='{provinsi}';
        """)

        restoran = dict_fetch_all(cursor)
        print(restoran)


        for i in range(len(restoran)):
            # get promo
            cursor.execute(f"""
                SELECT P.Promoname, P.id
                FROM (SELECT RName, RBranch, PId, RPromo_start, RPromo_end
                    FROM RESTAURANT NATURAL JOIN RESTAURANT_PROMO
                    WHERE province='{provinsi}') R LEFT OUTER JOIN PROMO P
                ON R.PId = P.id
                WHERE R.RPromo_start <= CURRENT_DATE AND R.RPromo_end >= CURRENT_DATE 
                AND R.RName='{restoran[i]['rname'].replace("'", "''")}' AND R.RBranch='{restoran[i]['rbranch']}';
            """)

            restoran[i]['promo'] = dict_fetch_all(cursor)
            restoran[i]['nomor'] = str(i+1)
        
        context['restoran'] = restoran
 
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
    return render(request, 'pilih_resto.html', context)

@csrf_exempt
def pilih_menu(request, rname, rbranch):
    email = request.COOKIES['email']
    transaksi = pelanggan[email]
    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }

    with connection.cursor() as cursor:
        # get food
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT RName, RBranch, Foodname, Price, Stock
            FROM FOOD
            WHERE RName='{rname.replace("'", "''")}' AND RBranch='{rbranch}';
        """)

        menu = dict_fetch_all(cursor)
        print(menu)
        context['menu'] = menu
        for i in range(len(menu)):
            context['menu'][i]['nomor'] = str(i+1)

        # get payment methods
        cursor.execute(f"""
            SELECT id, name
            FROM PAYMENT_METHOD;
        """)

        metode_pembayaran = dict_fetch_all(cursor)
        context['metode_pembayaran'] = metode_pembayaran

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    if request.method == 'POST':

        # check if customer order something
        memesan = False
        total_food = 0
        transaksi.data['food'] = {}
        for m in menu:
            jumlah = int(request.POST.get(f'jumlah_{m["foodname"]}'))
            if jumlah > 0:
                memesan = True
                total_food += m['price'] * jumlah
                catatan = request.POST.get(f'catatan_{m["foodname"]}')
                transaksi.data['food'][m["foodname"]] = [jumlah, catatan]

        if memesan:
            # store temporary data
            transaksi.data['p_method'] = request.POST.get('pembayaran').split('_')
            transaksi.data['date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            # insert data
            with connection.cursor() as cursor:
                email = request.COOKIES['email']
                date_time = transaksi.data['date_time']
                street = transaksi.data['street']
                district = transaksi.data['district']
                city = transaksi.data['city']
                province = transaksi.data['province']
                total_food = total_food
                total_discount = 0
                delivery_fee = 0
                total_price = 0
                pmid = transaksi.data['p_method'][0]
                psid = 'PS1'
                dfid = transaksi.data['id_province']
                vehicletype = request.POST.get('pengantaran')

                # insert transaction data
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                    INSERT INTO TRANSACTION (email, datetime, street, district, city, province, totalfood, totaldiscount, 
                    deliveryfee, totalprice, pmid, psid, dfid, vehicletype) VALUES 
                    ('{email}', '{date_time}', '{street}', '{district}', '{city}', '{province}', {total_food}, {total_discount}, 
                    {delivery_fee}, {total_price}, '{pmid}', '{psid}', '{dfid}', '{vehicletype}');
                """)

                for key, value in transaksi.data['food'].items():
                    # insert transaction food data
                    cursor.execute(f"""
                        INSERT INTO TRANSACTION_FOOD VALUES 
                        ('{email}', '{date_time}', '{rname}', '{rbranch}', '{key}', {value[0]}, '{value[1]}');
                    """)

                # insert transaction history
                cursor.execute(f"""
                    INSERT INTO TRANSACTION_HISTORY VALUES
                    ('{email}', '{date_time}', 'TS1', '{date_time}'); 
                """)
                
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            return redirect('TransaksiPelanggan:daftar_pesanan')
        else:
            messages.info(request, 'Belum ada menu yang di pilih!')

    return render(request, 'pilih_menu.html', context)

def daftar_pesanan(request):
    email = request.COOKIES['email']
    transaksi = pelanggan[email]
    date_time = transaksi.data['date_time']

    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }
    with connection.cursor() as cursor:
        # get transaction food data
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT * FROM TRANSACTION_FOOD NATURAL JOIN FOOD
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        menu = dict_fetch_all(cursor)
        context['menu'] = menu
        for i in range(len(menu)):
            context['menu'][i]['nomor'] = str(i+1)
            context['menu'][i]['total'] = context['menu'][i]['price'] * context['menu'][i]['amount']

        # get transaction data
        cursor.execute(f"""
            SELECT * FROM TRANSACTION
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        transaction = dict_fetch_all(cursor)
        transaction = transaction[0]
        context['transaction'] = transaction

        # get payment method
        cursor.execute(f"""
            SELECT name FROM PAYMENT_METHOD
            WHERE id='{transaction['pmid']}'; 
        """)

        payment_method = dict_fetch_all(cursor)
        context['payment_method'] = payment_method[0]

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
    
    return render(request, 'daftar_pesanan.html', context)

def konfirmasi_pembayaran(request):
    email = request.COOKIES['email']
    transaksi = pelanggan[email]
    date_time = transaksi.data['date_time']

    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }
    with connection.cursor() as cursor:
        # get transaction food data
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT * FROM TRANSACTION_FOOD NATURAL JOIN FOOD
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        menu = dict_fetch_all(cursor)
        context['menu'] = menu
        for i in range(len(menu)):
            context['menu'][i]['nomor'] = str(i+1)
            context['menu'][i]['total'] = context['menu'][i]['price'] * context['menu'][i]['amount']

        # get restaurant data
        cursor.execute(f"""
            SELECT * FROM RESTAURANT
            WHERE rname='{menu[0]['rname']}' AND rbranch='{menu[0]['rbranch']}'; 
        """)

        restaurant = dict_fetch_all(cursor)
        restaurant = restaurant[0]
        context['restaurant'] = restaurant

        # get transaction data
        cursor.execute(f"""
            SELECT * 
            FROM ((TRANSACTION NATURAL JOIN USER_ACC) 
                NATURAL JOIN TRANSACTION_HISTORY) T 
                JOIN PAYMENT_METHOD P
            ON T.pmid=P.id
            WHERE T.email='{email}' AND T.datetime='{date_time}'; 
        """)

        transaction = dict_fetch_all(cursor)
        transaction = transaction[0]
        context['transaction'] = transaction

        # get payment method
        cursor.execute(f"""
            SELECT name FROM PAYMENT_STATUS
            WHERE id='{transaction['psid']}'; 
        """)

        payment_status = dict_fetch_all(cursor)
        payment_status = payment_status[0]
        context['payment_status'] = payment_status

        # get transaction status
        cursor.execute(f"""
            SELECT name FROM TRANSACTION_STATUS
            WHERE id='{transaction['tsid']}'; 
        """)

        transaction_status = dict_fetch_all(cursor)
        transaction_status = transaction_status[0]
        context['transaction_status'] = transaction_status

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    return render(request, 'konfirmasi_pembayaran.html', context)

def bayar(request):
    email = request.COOKIES['email']
    transaksi = pelanggan[email]
    date_time = transaksi.data['date_time']
    payment_method = transaksi.data['p_method'][1]
    
    with connection.cursor() as cursor:
        # get transaction data
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT * FROM TRANSACTION
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        transaction = dict_fetch_all(cursor)
        transaction = transaction[0]

        if payment_method == 'RestoPay':
            try: 
                # update RestoPay
                cursor.execute(f"""
                UPDATE TRANSACTION_ACTOR
                SET RestoPay=RestoPay - {transaction['totalprice']}
                WHERE email='{email}'; 
                """)
            except Exception as e:
                print(e)
                res = str(e).split("\n")[0]
                messages.info(request, res)
                return redirect('TransaksiPelanggan:konfirmasi_pembayaran')
        
        # get payment status id and update psid in transaction
        cursor.execute(f"""
            SELECT id FROM PAYMENT_STATUS
            WHERE name='Berhasil'; 
        """)
        psid = dict_fetch_all(cursor)
        psid = psid[0]['id']

        cursor.execute(f"""
        UPDATE TRANSACTION
        SET psid='{psid}'
        WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        # get all transaction food and update stock
        cursor.execute(f"""
            SELECT * FROM TRANSACTION_FOOD
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        menu = dict_fetch_all(cursor)

        for m in menu:
            cursor.execute(f"""
            UPDATE FOOD
            SET stock=stock - {m['amount']}
            WHERE rname='{m['rname']}' AND rbranch='{m['rbranch']}' AND foodname='{m['foodname']}'; 
            """)

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        del pelanggan[email]
        return ringkasan_pesanan(request, email, date_time)

def gagal_bayar(request):
    email = request.COOKIES['email']
    transaksi = pelanggan[email]
    date_time = transaksi.data['date_time']

    with connection.cursor() as cursor:
        # get payment status id and update psid in transaction
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT id FROM PAYMENT_STATUS
            WHERE name='Gagal'; 
        """)
        psid = dict_fetch_all(cursor)
        psid = psid[0]['id']

        cursor.execute(f"""
        UPDATE TRANSACTION
        SET psid='{psid}'
        WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        # get transaction status id and update tsid in transaction history
        cursor.execute(f"""
            SELECT id FROM TRANSACTION_STATUS
            WHERE name='Pesanan Dibatalkan'; 
        """)
        tsid = dict_fetch_all(cursor)
        tsid = tsid[0]['id']

        cursor.execute(f"""
        UPDATE TRANSACTION_HISTORY
        SET tsid='{tsid}', datetimestatus='{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
    del pelanggan[email]
    return redirect('authentication:dashboard')

def ringkasan_pesanan(request, email, date_time):
    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }
    with connection.cursor() as cursor:
        # get transaction food data
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT * FROM TRANSACTION_FOOD NATURAL JOIN FOOD
            WHERE email='{email}' AND datetime='{date_time}'; 
        """)

        menu = dict_fetch_all(cursor)
        context['menu'] = menu
        for i in range(len(menu)):
            context['menu'][i]['nomor'] = str(i+1)
            context['menu'][i]['total'] = context['menu'][i]['price'] * context['menu'][i]['amount']

        # get restaurant data
        cursor.execute(f"""
            SELECT * FROM RESTAURANT
            WHERE rname='{menu[0]['rname']}' AND rbranch='{menu[0]['rbranch']}'; 
        """)

        restaurant = dict_fetch_all(cursor)
        restaurant = restaurant[0]
        context['restaurant'] = restaurant

        # get transaction data
        cursor.execute(f"""
            SELECT * 
            FROM ((TRANSACTION NATURAL JOIN USER_ACC) NATURAL JOIN TRANSACTION_HISTORY) T JOIN PAYMENT_METHOD P
            ON T.pmid=P.id
            WHERE T.email='{email}' AND T.datetime='{date_time}'; 
        """)

        transaction = dict_fetch_all(cursor)
        transaction = transaction[0]
        context['transaction'] = transaction

        # get payment status
        cursor.execute(f"""
            SELECT name FROM PAYMENT_STATUS
            WHERE id='{transaction['psid']}'; 
        """)

        payment_status = dict_fetch_all(cursor)
        payment_status = payment_status[0]
        context['payment_status'] = payment_status

        # get transaction status
        cursor.execute(f"""
            SELECT name FROM TRANSACTION_STATUS
            WHERE id='{transaction['tsid']}'; 
        """)

        transaction_status = dict_fetch_all(cursor)
        transaction_status = transaction_status[0]
        context['transaction_status'] = transaction_status

        # get courier data
        cursor.execute(f"""
            SELECT * 
            FROM COURIER NATURAL JOIN USER_ACC
            WHERE email='{transaction['courierid']}'; 
        """)

        courier = dict_fetch_all(cursor)
        if len(courier) > 0:
            courier = courier[0]
        else:
            courier = {
                'fname':'-',
                'lname':'',
                'platenum':'-',
                'vehicletype':'-',
                'vehiclebrand':'-'
            }
        context['courier'] = courier

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
    return render(request, 'ringkasan_pesanan.html', context)

def pesanan_berlangsung(request):
    email = request.COOKIES['email']
    
    context = {
        'user': {'role': f'{get_user_role(email)}'}
    }

    with connection.cursor() as cursor:
        # get ongoing transaction data
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            SELECT R.rname as rname, R.rbranch as rbranch, T.datetime as datetime, T.email as email, S.status as status 
            FROM (SELECT * FROM TRANSACTION_HISTORY
                WHERE email='{email}') T, 
                (SELECT DISTINCT datetime, rname, rbranch
                FROM TRANSACTION_FOOD
                WHERE email='{email}') R, 
                (SELECT TR.datetime as datetime, ST.name as status
                FROM TRANSACTION_HISTORY TR JOIN TRANSACTION_STATUS ST
                ON TR.tsid=ST.id
                WHERE TR.email='{email}') S
            WHERE T.datetime=R.datetime AND T.datetime=S.datetime AND T.tsid NOT IN (
                SELECT id
                FROM TRANSACTION_STATUS
                WHERE name='Pesanan Dibatalkan' OR name='Pesanan Selesai'); 
        """)

        transaction = dict_fetch_all(cursor)
        context['transaction'] = transaction
        for i in range(len(transaction)):
            context['transaction'][i]['nomor'] = str(i+1)

        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    return render(request, 'pesanan_berlangsung.html', context)