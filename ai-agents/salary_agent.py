import os
import logging
from datetime import datetime, timedelta
from utils import get_config, get_weekly_revenue, initiate_bank_transfer, send_email

# Configure logging
logging.basicConfig(filename='salary.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = get_config()

def calculate_salary():
    """Calculate owner's weekly salary"""
    logging.info("Calculating owner salary")
    
    # Get weekly revenue
    revenue = get_weekly_revenue()
    
    # Calculate expenses
    expenses = calculate_expenses()
    
    # Calculate salary (65% of revenue minus expenses)
    salary = (revenue * 0.65) - expenses
    
    logging.info(f"Revenue: R{revenue}, Expenses: R{expenses}, Salary: R{salary}")
    return salary

def calculate_expenses():
    """Calculate weekly business expenses"""
    # This would query actual expenses from accounting system
    return 3500  # Simplified for example

def pay_owner_salary():
    """Initiate salary payment to owner"""
    salary = calculate_salary()
    if salary <= 0:
        logging.warning("No salary to pay this week")
        return False
    
    # Initiate bank transfer
    success = initiate_bank_transfer(
        CONFIG['owner_bank_account'],
        salary,
        "Weekly Salary - Empowering Moms"
    )
    
    if success:
        logging.info(f"Salary payment of R{salary} initiated")
        send_confirmation(salary)
        return True
    else:
        logging.error("Salary payment failed")
        return False

def send_confirmation(amount):
    """Send payment confirmation to owner"""
    subject = "Salary Payment Confirmation"
    body = f"Your weekly salary of R{amount:.2f} has been transferred to your bank account."
    send_email(CONFIG['owner_email'], subject, body)

if __name__ == "__main__":
    # Run every Friday
    if datetime.now().weekday() == 4:  # Friday
        pay_owner_salary()
