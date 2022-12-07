from django.shortcuts import render
from django.db import connection
import json

# Create your views here.

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def show_tarif(request):
    
    context = {
        "user": {
            'role': 'Admin'
        }
    }
    
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM DELIVERY_FEE_PER_KM;
                """)
        delivery_fee_per_km = dictfetchall(cursor)
        dump = json.dumps(delivery_fee_per_km)
        context['delivery_fee_per_km'] = dump

    counter = 0
    for i in delivery_fee_per_km:
        counter += 1
        context[f'deliveryId{counter}'] = i["id"];
        context[f'deliveryProvince{counter}'] = i["province"];
        context[f'deliveryMotorfee{counter}'] = i["motorfee"];
        context[f'deliveryCarFee{counter}'] = i["carfee"];

    context['delivery_fee_per_km_nodump'] = delivery_fee_per_km
    context['delivery_length'] = counter
    return render(request, 'show_tarif.html', context)

def create_tarif(request):
    context = {
        "user": {
            'role': 'Admin'
        }
    }


    return render(request, 'create_tarif.html', context)