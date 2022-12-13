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

def check_user_availability(email, password):
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO SIREST;')
        cursor.execute(f'''
            SELECT *
            FROM USER_ACC
            WHERE Email='{email}' AND Password='{password}';
        ''')
        user_list = dict_fetch_all(cursor)
    if len(user_list) != 0: # User found
        return True
    else: # User not found
        return False

def get_rname_rbranch(email):
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO SIREST;')
        cursor.execute(f'''
            SELECT RName, RBranch
            FROM RESTAURANT
            WHERE Email='{email}';
        ''')
        user_list = dict_fetch_all(cursor)
    if len(user_list) != 0: # User found
        return (user_list[0]['rname'], user_list[0]['rbranch'])
    else: # User not found
        return (None, None)