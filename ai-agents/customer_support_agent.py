import os
import logging
import smtplib
from email.mime.text import MIMEText
from utils import get_config, generate_ai_response, get_unanswered_emails, mark_email_as_answered

# Configure logging
logging.basicConfig(filename='support.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = get_config()

def handle_customer_inquiries():
    """Process and respond to customer inquiries"""
    logging.info("Checking for new customer inquiries")
    emails = get_unanswered_emails()
    
    if not emails:
        logging.info("No new customer inquiries")
        return
    
    for email in emails:
        try:
            response = generate_ai_response(
                email['body'],
                context="You are a customer support agent for Empowering Moms, a platform offering online courses for South African mothers. Respond helpfully and professionally."
            )
            
            send_email_response(email['from'], response)
            mark_email_as_answered(email['id'])
            logging.info(f"Responded to inquiry from {email['from']}")
        except Exception as e:
            logging.error(f"Error processing email {email['id']}: {str(e)}")

def send_email_response(to_address, content):
    """Send email response to customer"""
    msg = MIMEText(content)
    msg['Subject'] = 'Re: Your Inquiry - Empowering Moms'
    msg['From'] = CONFIG['email']['support_address']
    msg['To'] = to_address
    
    with smtplib.SMTP(CONFIG['email']['smtp_server'], CONFIG['email']['smtp_port']) as server:
        server.starttls()
        server.login(CONFIG['email']['username'], CONFIG['email']['password'])
        server.send_message(msg)

def handle_refunds():
    """Automatically process refund requests"""
    logging.info("Processing refund requests")
    # Integration with payment system to handle refunds
    # Would include validation and processing logic

def run_support_chatbot():
    """Run AI-powered chatbot for real-time support"""
    logging.info("Starting support chatbot")
    # Implementation would integrate with website chat widget

if __name__ == "__main__":
    handle_customer_inquiries()
    handle_refunds()
