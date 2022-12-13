from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.urls import reverse

from utils.db_utils import *
from utils.users import *

import functools

DAYS = {
    'Senin': 0,
    'Selasa': 1,
    'Rabu': 2,
    'Kamis': 3,
    'Jumat': 4,
    'Sabtu': 5,
    'Minggu': 6
}

def compare_dict_with_day(dict1, dict2):
    return DAYS[dict1['day']] - DAYS[dict2['day']]

DUMMY_LIST = [
    {
        'id': 1,
        'hari' : 'Senin',
        'jam_buka' : '08:00:00',
        'jam_tutup' : '21:00:00',
    },
    {
        'id': 2,
        'hari' : 'Selasa',
        'jam_buka': '08:30:00',
        'jam_tutup': '22:00:00',
    },
    {
        'id': 3,
        'hari' : 'Rabu',
        'jam_buka': '13:00:00',
        'jam_tutup': '23:00:00',
    },
]

# Create your views here.
def jam_operasional_buat(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'Restoran':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    if request.method == 'GET':
        context = {
            'user': {
                'role': get_user_role(email),
            },
        }
        return render(request, 'jam_operasional_buat.html', context)
    elif request.method == 'POST':
        day = request.POST.get('day', None)
        start_hours = request.POST.get('start_hours', None)
        end_hours = request.POST.get('end_hours', None)
        if day == None or start_hours == None or end_hours == None:
            return HttpResponse(status=400)
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    INSERT INTO RESTAURANT_OPERATING_HOURS VALUES
                    ('{restaurant_name}', '{restaurant_branch}', '{day}', '{start_hours}', '{end_hours}');
                ''')
            return HttpResponse(status=201)
        except Exception as e:
            return HttpResponse(status=400)
    return HttpResponse(status=404)

def jam_operasional_daftar(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'Restoran':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT Day, StartHours, EndHours
                    FROM RESTAURANT_OPERATING_HOURS
                    WHERE Name='{restaurant_name}'
                        AND Branch='{restaurant_branch}';
                ''')
                hours_list = dict_fetch_all(cursor)
                for i in range(len(hours_list)):
                    hours_list[i]['formattedstarthours'] = hours_list[i]['starthours'].strftime('%H:%M:%S')
                    hours_list[i]['formattedendhours'] = hours_list[i]['endhours'].strftime('%H:%M:%S')
                hours_list.sort(key=functools.cmp_to_key(compare_dict_with_day))
        except Exception as e:
            return HttpResponse(status=500)
        context = {
            'hours_list': hours_list,
            'user': {
                'role': get_user_role(email),
            },
        }
        return render(request, 'jam_operasional_daftar.html', context)
    return HttpResponse(status=404)

def jam_operasional_ubah(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'Restoran':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        # Get Parameters
        day = request.GET.get('day', '')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    SELECT Day, StartHours, EndHours
                    FROM RESTAURANT_OPERATING_HOURS
                    WHERE Day='{day}'
                        AND Name='{restaurant_name}'
                        AND Branch='{restaurant_branch}';
                ''')
                hours_list = dict_fetch_all(cursor)
                if len(hours_list) == 0:
                    raise Exception('Operating Hours Not Found')
                hour = hours_list[0]
                hour['formattedstarthours'] = hour['starthours'].strftime('%H:%M:%S')
                hour['formattedendhours'] = hour['endhours'].strftime('%H:%M:%S')
        except Exception as e:
            return HttpResponse(status=404)
        context = {
            'day': day,
            'start_hours': hour['formattedstarthours'],
            'end_hours': hour['formattedendhours'],
            'user': {
                'role': get_user_role(email),
            },
        }
        return render(request, 'jam_operasional_ubah.html', context)
    elif request.method == 'PUT':
        put = QueryDict(request.body)
        day = put.get('day', None)
        start_hours = put.get('start_hours', None)
        end_hours = put.get('end_hours', None)
        if day == None or start_hours == None or end_hours == None:
            return HttpResponse(status=400)
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    UPDATE RESTAURANT_OPERATING_HOURS
                    SET StartHours='{start_hours}', EndHours='{end_hours}'
                    WHERE Name='{restaurant_name}' AND Branch='{restaurant_branch}' AND DAY='{day}';
                ''')
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)
    return HttpResponse(status=404)

def jam_operasional_hapus(request):
    email = request.COOKIES.get('email')
    password = request.COOKIES.get('password')
    if not check_user_availability(email, password):
        return HttpResponse(status=404)
    if get_user_role(email) != 'Restoran':
        return HttpResponse(status=404)
    (restaurant_name, restaurant_branch) = get_rname_rbranch(email)
    if restaurant_name is None or restaurant_branch is None:
        return HttpResponse(status=404)
    
    if request.method == 'DELETE':
        delete = QueryDict(request.body)
        day = delete.get('day', '')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET SEARCH_PATH TO SIREST;')
                cursor.execute(f'''
                    DELETE FROM RESTAURANT_OPERATING_HOURS
                    WHERE Name='{restaurant_name}' AND Branch='{restaurant_branch}' AND DAY='{day}';
                ''')
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
    return HttpResponse(status=404)