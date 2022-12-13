from django.shortcuts import render
from django.db import connection
from utils.db_utils import dict_fetch_all
import json

# Create your views here.
def show_detail_restoran(request, id):
    context = {
        "user": {
            'role': 'Pelanggan'
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM RESTAURANT;
                """)
        restaurant = dict_fetch_all(cursor)
        restaurant = restaurant[id-1]
        dumps = json.dumps(restaurant)
        context['restaurant'] = dumps
    
    rname = restaurant['rname']
    rbranch = restaurant['rbranch']

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM RESTAURANT_OPERATING_HOURS
                    WHERE Name = '{rname}' AND Branch = '{rbranch}';
                """)
        restaurant_operating_hours = dict_fetch_all(cursor)
        context['restaurant_operating_hours_no_dumps'] = restaurant_operating_hours
        # dumps = json.dumps(restaurant_operating_hours)
        # context['restaurant_operating_hours'] = dumps
        
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT P.PromoName
                    FROM RESTAURANT_PROMO RP, PROMO P
                    WHERE RP.RName = '{rname}' AND RP.RBranch = '{rbranch}' AND RP.PId = P.id AND (CURRENT_TIMESTAMP BETWEEN RP.rpromo_start AND RP.rpromo_end);
                """)
        restaurant_promo = dict_fetch_all(cursor)
        context['restaurant_promo_no_dumps'] = restaurant_promo

    context['restaurant_no_dumps'] = restaurant

    return render(request, 'detail_restoran.html', context)

def show_daftar_restoran(request):
    context = {
        "user": {
            'role': 'Pelanggan'
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM RESTAURANT;
                """)
        restaurant = dict_fetch_all(cursor)
        dumps = json.dumps(restaurant)
        context['restaurant'] = dumps
    context['restaurant_no_dumps'] = restaurant

    return render(request, 'daftar_restoran.html', context)
