# scripts/ai_agents/salary_calculator.py
import requests
from datetime import datetime, timedelta
from scripts.utils import get_weekly_revenue, initiate_bank_transfer

def calculate_salary():
    revenue = get_weekly_revenue()
    expenses = 0  # Calculate expenses (AI costs, hosting, etc.)
    salary = revenue * 0.65 - expenses  # 35% reinvestment
    return salary

def pay_owner():
    salary = calculate_salary()
    # Initiate transfer to owner's bank account
    result = initiate_bank_transfer(salary, "owner_bank_account")
    # Send confirmation
    if result:
        send_email("owner@example.com", "Salary Paid", f"Your salary of R{salary} has been transferred.")

if __name__ == "__main__":
    pay_owner()
