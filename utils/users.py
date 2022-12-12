from django.db import connection
from utils.db_utils import dict_fetch_all

def get_user_role(email):    
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO SIREST;')
        # Check Admin
        cursor.execute(f'''
            SELECT *
            FROM ADMIN
            WHERE Email='{email}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'Admin'
    
        # Check Courier
        cursor.execute(f'''
            SELECT *
            FROM COURIER
            WHERE Email='{email}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'Kurir'
    
        # Check Customer
        cursor.execute(f'''
            SELECT *
            FROM CUSTOMER
            WHERE Email='{email}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'Pelanggan'
    
        # Check Restaurant
        cursor.execute(f'''
            SELECT *
            FROM RESTAURANT
            WHERE Email='{email}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'Restoran'
    
    return 'none'