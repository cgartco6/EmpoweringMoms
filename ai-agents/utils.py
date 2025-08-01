import os
import json
import smtplib
import logging
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load configuration
def get_config():
    """Load configuration from file"""
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "website_url": "https://empoweringmoms.co.za",
            "owner_email": "owner@example.com",
            "owner_bank_account": "1234567890",
            "courses": {
                "facebook_blueprint": 500,
                "academy_six": 1800,
                "little_learners": 250
            },
            "ai_api_key": os.getenv("AI_API_KEY"),
            "payfast": {
                "merchant_id": os.getenv("PAYFAST_MERCHANT_ID"),
                "merchant_key": os.getenv("PAYFAST_MERCHANT_KEY"),
                "process_url": "https://www.payfast.co.za/eng/process"
            }
        }

def generate_ai_content(prompt, content_type="text", max_tokens=500):
    """Generate content using AI API"""
    api_key = get_config().get('ai_api_key')
    if not api_key:
        raise ValueError("AI API key not configured")
    
    if content_type == "text":
        endpoint = "https://api.openai.com/v1/completions"
        payload = {
            "model": "gpt-4",
            "prompt": prompt,
            "max_tokens": max_tokens
        }
    elif content_type == "image":
        endpoint = "https://api.deepai.org/api/text2img"
        payload = {"text": prompt}
    else:
        raise ValueError("Unsupported content type")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(endpoint, json=payload, headers=headers)
    
    if response.status_code == 200:
        if content_type == "text":
            return response.json()['choices'][0]['text']
        elif content_type == "image":
            return response.json()['output_url']
    else:
        raise Exception(f"AI API error: {response.text}")

def send_email(to, subject, body):
    """Send email notification"""
    config = get_config().get('email', {})
    msg = MIMEMultipart()
    msg['From'] = config.get('from_address', 'noreply@empoweringmoms.co.za')
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port', 587)) as server:
            server.starttls()
            server.login(config.get('username'), config.get('password'))
            server.send_message(msg)
        return True
    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        return False

def send_alert(subject, message):
    """Send critical alert to admin"""
    admin_email = get_config().get('admin_email', 'admin@example.com')
    send_email(admin_email, f"ALERT: {subject}", message)

def log_transaction(transaction):
    """Log payment transaction to database"""
    # Implementation would save to database
    pass

def initiate_bank_transfer(account_number, amount, description):
    """Initiate bank transfer using banking API"""
    # Implementation would use bank API
    return True  # Simplified for example

# Additional utility functions would be added as needed
