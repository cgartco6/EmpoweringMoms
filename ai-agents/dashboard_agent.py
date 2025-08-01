import os
import logging
import json
from datetime import datetime, timedelta
from utils import get_config, query_database, send_email_with_attachment

# Configure logging
logging.basicConfig(filename='dashboard.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = get_config()

def generate_dashboard_data():
    """Collect and format data for the owner dashboard"""
    logging.info("Generating dashboard data")
    
    # Calculate date ranges
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get revenue data
    revenue_data = get_revenue_data(start_date, end_date)
    
    # Get enrollment data
    enrollment_data = get_enrollment_data(start_date, end_date)
    
    # Get marketing performance
    marketing_data = get_marketing_performance(start_date, end_date)
    
    # Compile dashboard data
    dashboard = {
        "revenue": revenue_data,
        "enrollments": enrollment_data,
        "marketing": marketing_data,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to database
    save_to_database("dashboard_snapshots", dashboard)
    
    logging.info("Dashboard data generated")
    return dashboard

def get_revenue_data(start_date, end_date):
    """Get revenue data by course, province, and date"""
    # Query database for revenue metrics
    return {
        "total": 42000,
        "by_course": {
            "academy_six": 18000,
            "facebook_blueprint": 15000,
            "little_learners": 9000
        },
        "by_province": {
            "Gauteng": 15000,
            "Western Cape": 12000,
            "KwaZulu-Natal": 8000,
            "Eastern Cape": 4000,
            "Free State": 3000
        },
        "by_date": {
            "2025-07-01": 1200,
            "2025-07-02": 1500,
            # ... more dates
        }
    }

def get_enrollment_data(start_date, end_date):
    """Get course enrollment metrics"""
    return {
        "total": 142,
        "by_course": {
            "academy_six": 14,
            "facebook_blueprint": 85,
            "little_learners": 43
        },
        "by_source": {
            "facebook": 65,
            "instagram": 42,
            "tiktok": 25,
            "direct": 10
        }
    }

def get_marketing_performance(start_date, end_date):
    """Get marketing campaign performance"""
    return {
        "roi": {
            "facebook": 4.2,
            "instagram": 3.8,
            "tiktok": 5.1
        },
        "conversion_rates": {
            "facebook": 2.4,
            "instagram": 1.8,
            "tiktok": 3.2
        },
        "cost_per_acquisition": {
            "facebook": 120,
            "instagram": 150,
            "tiktok": 95
        }
    }

def send_daily_report():
    """Send daily report to business owner"""
    logging.info("Sending daily report")
    data = generate_dashboard_data()
    
    # Generate PDF report
    pdf_path = generate_pdf_report(data)
    
    # Send email
    send_email_with_attachment(
        CONFIG['owner_email'],
        "Daily Business Report - Empowering Moms",
        "Attached is your daily business report",
        pdf_path
    )
    logging.info("Daily report sent")

def generate_pdf_report(data):
    """Generate PDF version of dashboard report"""
    # Implementation would use a PDF generation library
    return "/path/to/report.pdf"

if __name__ == "__main__":
    send_daily_report()
