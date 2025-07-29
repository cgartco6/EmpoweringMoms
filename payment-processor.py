import os
import sqlite3
import requests
from datetime import datetime

# PayFast integration
def process_payment(transaction_id, amount, course_id, user_data):
    PAYFAST_MERCHANT_ID = os.getenv('PAYFAST_MERCHANT_ID')
    PAYFAST_MERCHANT_KEY = os.getenv('PAYFAST_MERCHANT_KEY')
    
    payload = {
        'merchant_id': PAYFAST_MERCHANT_ID,
        'merchant_key': PAYFAST_MERCHANT_KEY,
        'amount': str(amount),
        'item_name': course_id,
        'return_url': 'https://yourdomain.com/success',
        'cancel_url': 'https://yourdomain.com/cancel',
        'notify_url': 'https://yourdomain.com/notify',
        'email_address': user_data['email'],
        'name_first': user_data['name'].split()[0],
        'name_last': user_data['name'].split()[-1],
        'cell_number': user_data['phone']
    }
    
    response = requests.post('https://www.payfast.co.za/eng/process', data=payload)
    if response.status_code == 200:
        record_transaction(transaction_id, amount, course_id, user_data)
        return response.url
    return None

def record_transaction(transaction_id, amount, course_id, user_data):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT, date TEXT, amount REAL, course TEXT, 
                 name TEXT, email TEXT, phone TEXT, province TEXT)''')
    
    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (transaction_id, datetime.now().isoformat(), amount, course_id,
               user_data['name'], user_data['email'], user_data['phone'], user_data['province']))
    conn.commit()
    conn.close()

def generate_dashboard_data():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    
    # Revenue by province
    c.execute("SELECT province, SUM(amount) FROM transactions GROUP BY province")
    province_data = c.fetchall()
    
    # Revenue by course
    c.execute("SELECT course, SUM(amount) FROM transactions GROUP BY course")
    course_data = c.fetchall()
    
    # Weekly salary calculation
    c.execute("SELECT SUM(amount) FROM transactions WHERE date > date('now','-7 days')")
    weekly_revenue = c.fetchone()[0] or 0
    salary = weekly_revenue * 0.65  # 35% reinvestment
    
    return {
        'province_revenue': dict(province_data),
        'course_revenue': dict(course_data),
        'salary': salary
    }
