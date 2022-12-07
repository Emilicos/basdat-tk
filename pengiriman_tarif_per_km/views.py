from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, JsonResponse
import json
import random
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def update_tarif(request):
    if(request.method == "POST"):
        id = request.POST.get("id")
        motorfee = request.POST.get("motorfee")
        carfee = request.POST.get("carfee")
    
        with connection.cursor() as cursor:
            try: 
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                UPDATE DELIVERY_FEE_PER_KM SET motorFee = {motorfee}, carFee = {carfee} WHERE id = '{id}';""")

                cursor.execute("SET SEARCH_PATH TO PUBLIC")
                return JsonResponse({
                    "message": "Successful"
                })
            except Exception as e:
                print(e)
                res = str(e).split("\n")[0]
                return JsonResponse({
                    "message": res
                })

@csrf_exempt
def show_create_tarif(request):
    context = {
        "user": {
            'role': 'Admin'
        }
    }
    
    if(request.method == "POST"):
        province = request.POST.get("province")
        motorfee = request.POST.get("motorfee")
        carfee = request.POST.get("carfee")
        id = "D" + f"{random.randint(1, 1000000)}"
        
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                        SELECT *
                        FROM DELIVERY_FEE_PER_KM;
                    """)
            delivery_fee_per_km = dictfetchall(cursor)
            listOfId = []
            for item in delivery_fee_per_km:
                listOfId.append(item["id"])
            while(id in listOfId):  
                id = "D" + f"{random.randint(1, 1000000)}"
            
            cursor.execute("SET SEARCH_PATH TO PUBLIC")
        with connection.cursor() as cursor:
            try: 
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                INSERT INTO DELIVERY_FEE_PER_KM VALUES
                ('{id}', '{province}', {motorfee}, {carfee});
                 """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC")
                return JsonResponse({
                    "message": "Successful"
                })
            except Exception as e:
                res = str(e).split("\n")[0]
                return JsonResponse({
                    "message": res
                })
    else:                
        return render(request, 'create_tarif.html', context)

def delete_tarif(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM DELIVERY_FEE_PER_KM
            WHERE id='{id}';
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC")

    return redirect('tarif:show_tarif')