import os
import logging
import requests
from utils import get_config, log_transaction, send_alert

# Configure logging
logging.basicConfig(filename='payments.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = get_config()

def process_payment(transaction_data):
    """Process payment transaction securely"""
    logging.info(f"Processing payment for {transaction_data['email']}")
    
    # Validate transaction
    if not validate_transaction(transaction_data):
        logging.warning("Invalid transaction detected")
        return False
    
    # Process with PayFast (South African payment gateway)
    payload = {
        'merchant_id': CONFIG['payfast']['merchant_id'],
        'merchant_key': CONFIG['payfast']['merchant_key'],
        'amount': transaction_data['amount'],
        'item_name': transaction_data['course_name'],
        'return_url': f"{CONFIG['website_url']}/success",
        'cancel_url': f"{CONFIG['website_url']}/cancel",
        'notify_url': f"{CONFIG['website_url']}/webhook/payfast",
        'email_address': transaction_data['email'],
        'm_payment_id': transaction_data['id']
    }
    
    try:
        response = requests.post(CONFIG['payfast']['process_url'], data=payload)
        if response.status_code == 200:
            log_transaction(transaction_data)
            grant_course_access(transaction_data['email'], transaction_data['course_id'])
            logging.info("Payment processed successfully")
            return True
    except Exception as e:
        logging.error(f"Payment processing failed: {str(e)}")
        send_alert("Payment Error", f"Payment failed for {transaction_data['email']}: {str(e)}")
    
    return False

def validate_transaction(transaction):
    """Validate transaction for security and legitimacy"""
    # Implement comprehensive validation:
    # - Fraud detection
    # - AVS checks
    # - Velocity checks
    return True  # Simplified for example

def grant_course_access(email, course_id):
    """Grant access to purchased course"""
    logging.info(f"Granting access to course {course_id} for {email}")
    # Implementation would add user to course access list

def handle_webhook(data):
    """Handle payment gateway webhook notifications"""
    logging.info("Processing payment webhook")
    # Verify signature
    # Update transaction status
    # Trigger course access

def generate_payment_reports():
    """Generate daily payment reports"""
    logging.info("Generating payment reports")
    # Query database for transactions
    # Generate CSV/PDF reports
    # Send to owner

if __name__ == "__main__":
    # This would typically be triggered by a web request
    pass
