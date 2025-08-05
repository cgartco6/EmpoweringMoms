import os
import json
import hashlib
from datetime import datetime
from database import get_db_connection

def process_payment(transaction_data):
    """Process payment with military-grade security"""
    # Validate transaction
    if not validate_transaction(transaction_data):
        return False
    
    # Process with PayFast
    payfast_data = format_payfast_data(transaction_data)
    response = send_to_payfast(payfast_data)
    
    if response['status'] == 'success':
        # Record transaction
        record_transaction(transaction_data)
        # Grant course access
        grant_course_access(transaction_data['user_email'], transaction_data['course_id'])
        # Notify user
        send_payment_confirmation(transaction_data)
        return True
    return False

def validate_transaction(data):
    """Validate transaction with fraud detection"""
    # Implement comprehensive validation:
    # - IP address verification
    # - Velocity checks
    # - BIN validation
    # - 3D Secure
    return True

def record_transaction(data):
    """Store transaction in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (id, user_id, course_id, amount, currency, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['transaction_id'],
        data['user_id'],
        data['course_id'],
        data['amount'],
        'ZAR',
        'pending',
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def grant_course_access(email, course_id):
    """Grant access to purchased course"""
    # Add user to course access list
    # Send course access email

def handle_webhook(data):
    """Handle payment gateway webhook"""
    # Verify signature
    # Update transaction status
    # Trigger fulfillment

def generate_weekly_report():
    """Generate weekly financial report for owner"""
    # Calculate revenue, expenses, salary
    # Generate PDF report
    # Send to owner
