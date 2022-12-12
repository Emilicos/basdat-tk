from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.db_utils import dict_fetch_all
import json

# Create your views here.

def getRNameandRBranch(request):
    email = request.COOKIES['email']
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT RName, RBranch
                    FROM RESTAURANT
                    WHERE email = '{email}';
                """)
        restaurant_data = dict_fetch_all(cursor)

    rname = restaurant_data[0]['rname']    
    rbranch = restaurant_data[0]['rbranch']

    return (rname, rbranch)

def get_makanan(rname, rbranch):
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
                    SELECT *
                    FROM FOOD
                    WHERE RName = '{rname}' AND rbranch = '{rbranch}';
                """)
        food = dict_fetch_all(cursor)
        for item in food:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT Name
                    FROM FOOD_CATEGORY
                    WHERE id = '{item['fcategory']}';
                """)
            food_category_name = dict_fetch_all(cursor)
            item['fcategory'] = food_category_name[0]['name']
            ingredientString = ""
            if(item['rname'] != "Venti's"):
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                        SELECT I.Name
                        FROM FOOD_INGREDIENT FI, INGREDIENT I
                        WHERE FI.RName = '{item['rname']}' AND FI.RBranch = '{item['rbranch']}' AND FI.FoodName = '{item['foodname']}' AND FI.Ingredient = I.id;
                    """)
                food_ingredient_name = dict_fetch_all(cursor)
                for i in range(len(food_ingredient_name)):
                    if(i != len(food_ingredient_name) - 1):
                        ingredientString += f"{food_ingredient_name[i]['name']}, "
                    else:
                        ingredientString += f"{food_ingredient_name[i]['name']}"
            else:
                ingredientString = "Kecap"

            item['ingredient'] = ingredientString
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                    SELECT *
                    FROM TRANSACTION_FOOD
                    WHERE rname = '{rname}' AND rbranch = '{rbranch}' AND foodname = '{item['foodname']}';
                """)
            transaction_food_data = dict_fetch_all(cursor)
            if(len(transaction_food_data) > 0):
                item['referred'] = True
            else:
                item['referred'] = False

        dumps = json.dumps(food)

    return [food, dumps]

def show_makanan_restoran(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }

    data_restaurant = getRNameandRBranch(request)
    rname = data_restaurant[0] 
    rbranch = data_restaurant[1]
    data = get_makanan(rname, rbranch)
    context["food_no_dumps"] = data[0]
    context["food"] = data[1]

    return render(request, 'show_makanan_restoran.html', context)

def show_makanan(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }
    rname = request.GET.get("param1").strip()
    rbranch = request.GET.get("param2").strip()
    
    data = get_makanan(rname, rbranch)
    context["food_no_dumps"] = data[0]
    context["food"] = data[1]

    return render(request, 'show_makanan.html', context)

@csrf_exempt
def create_makanan(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }
    if(request.method == "POST"):
        restaurant_data = getRNameandRBranch(request)
        rname = restaurant_data[0]
        rbranch = restaurant_data[1]

        foodname = request.POST.get("foodname")    
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        price = request.POST.get("price")
        fcategory = request.POST.get("fcategory")
        ingredient = request.POST.get("ingredient") # Push ke food_ingredient
        list_ingredient = ingredient.split(", ")
        with connection.cursor() as cursor:
            try: 
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                INSERT INTO FOOD VALUES
                ('{rname}', '{rbranch}', '{foodname}', '{description}', {stock}, {price}, '{fcategory}');
                 """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                for ingredient_item in list_ingredient:
                    cursor.execute("SET SEARCH_PATH TO SIREST;")
                    cursor.execute(f"""
                        INSERT INTO FOOD_INGREDIENT VALUES
                        ('{rname}', '{rbranch}', '{foodname}', '{ingredient_item}');
                    """)
                    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                return JsonResponse({
                    "message": "Successful"
                })
            except Exception as e:
                print(e)
                res = str(e).split("\n")[0]
                return JsonResponse({
                    "message": res
                })
    else:
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                        SELECT *
                        FROM INGREDIENT;
                    """)
            ingredient = dict_fetch_all(cursor)
            dumps = json.dumps(ingredient)
            context["ingredient"] = dumps
            context["ingredient_no_dumps"] = ingredient
        
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                        SELECT *
                        FROM FOOD_CATEGORY;
                    """)
            food_category = dict_fetch_all(cursor)
            dumps = json.dumps(food_category)
            context["food_category"] = dumps
            context["food_category_no_dumps"] = food_category

        return render(request, 'create_makanan.html', context)

def delete_food(request):
    rname = request.GET.get("param1").strip()
    rbranch = request.GET.get("param2").strip()
    foodname = request.GET.get("param3").strip()

    
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIREST;")
        cursor.execute(f"""
            DELETE FROM FOOD
            WHERE rname='{rname}' AND rbranch = '{rbranch}' AND foodname = '{foodname}';
        """)
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    return redirect('makanan:show_makanan_restoran')

@csrf_exempt
def update_makanan(request):
    context = {
        "user": {
            'role': 'Restoran'
        }
    }

    restaurant_data = getRNameandRBranch(request)
    rname = restaurant_data[0]
    rbranch = restaurant_data[1]
    context['rname'] = restaurant_data[0]
    context['rbranch'] = restaurant_data[1]
    if(request.method == "POST"):
        foodname = request.POST.get("foodname")    
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        price = request.POST.get("price")
        fcategory = request.POST.get("fcategory")
        ingredient = request.POST.get("ingredient") # Push ke food_ingredient
        list_ingredient = ingredient.split(", ")
        with connection.cursor() as cursor:
            try: 
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                DELETE FROM FOOD_INGREDIENT WHERE RName = '{rname}' AND RBranch = '{rbranch}' AND FoodName = '{foodname}';
                 """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")    
            
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                UPDATE FOOD SET description = '{description}', stock = {stock}, price = {price}, fcategory = '{fcategory}' WHERE RName = '{rname}' AND RBranch = '{rbranch}' AND FoodName = '{foodname}';
                 """)
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                for ingredient_item in list_ingredient:
                    cursor.execute("SET SEARCH_PATH TO SIREST;")
                    cursor.execute(f"""
                        INSERT INTO FOOD_INGREDIENT VALUES
                        ('{rname}', '{rbranch}', '{foodname}', '{ingredient_item}');
                    """)
                    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                return JsonResponse({
                    "message": "Successful"
                })
            except Exception as e:
                print(e)
                res = str(e).split("\n")[0]
                return JsonResponse({
                    "message": res
                })
    else:
        context['foodname'] = request.GET.get("foodname").strip()
        context['description'] = request.GET.get("description").strip()
        context['stock'] = request.GET.get("stock").strip()
        context['price'] = request.GET.get("price").strip()
        context['fcategory'] = request.GET.get("fcategory").strip()
        ingredient_name = request.GET.get("ingredient").strip()

        ingredient_name = ingredient_name.split(", ")

        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                        SELECT Id
                        FROM FOOD_CATEGORY
                        WHERE Name = '{context['fcategory']}';
                    """)
            food_category_name = dict_fetch_all(cursor)
            context["food_category_id"] = food_category_name[0]['id']

        counter = 0
        with connection.cursor() as cursor:
            for name in ingredient_name:
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                            SELECT *
                            FROM INGREDIENT
                            WHERE Name = '{name}';
                        """)
                ingredient_item = dict_fetch_all(cursor)
                if(counter > 0):
                    context['ingredient_item'] += ingredient_item
                else:
                    context['ingredient_item'] = ingredient_item
                counter +=  1
        ingredient_dumps = json.dumps(context['ingredient_item'])

        context['ingredient_dumps'] = ingredient_dumps

        with connection.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO SIREST;")
                cursor.execute(f"""
                            SELECT *
                            FROM INGREDIENT;
                        """)
                ingredient = dict_fetch_all(cursor)
                dumps = json.dumps(ingredient)
                context["ingredient"] = dumps
                context["ingredient_no_dumps"] = ingredient
            
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO SIREST;")
            cursor.execute(f"""
                        SELECT *
                        FROM FOOD_CATEGORY;
                    """)
            food_category = dict_fetch_all(cursor)
            dumps = json.dumps(food_category)
            context["food_category"] = dumps
            context["food_category_no_dumps"] = food_category

        return render(request, 'update_makanan.html', context)