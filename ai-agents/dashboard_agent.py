import sqlite3
import json
from datetime import datetime, timedelta

def generate_dashboard_data():
    """Generate data for the owner dashboard"""
    conn = sqlite3.connect('data/transactions.db')
    cursor = conn.cursor()
    
    # Get date ranges
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Revenue data
    cursor.execute("""
        SELECT DATE(created_at) AS date, SUM(amount) 
        FROM transactions 
        WHERE status = 'completed' AND created_at BETWEEN ? AND ?
        GROUP BY DATE(created_at)
    """, (start_date, end_date))
    revenue_data = cursor.fetchall()
    
    # Sales by province
    cursor.execute("""
        SELECT province, SUM(amount), COUNT(*) 
        FROM transactions 
        WHERE status = 'completed'
        GROUP BY province
    """)
    province_data = cursor.fetchall()
    
    # Course performance
    cursor.execute("""
        SELECT courses.title, SUM(transactions.amount), COUNT(*)
        FROM transactions
        JOIN courses ON transactions.course_id = courses.id
        WHERE transactions.status = 'completed'
        GROUP BY transactions.course_id
    """)
    course_data = cursor.fetchall()
    
    # Refund rate
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'refunded'")
    refunded = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]
    refund_rate = refunded / total if total > 0 else 0
    
    # Recent transactions
    cursor.execute("""
        SELECT id, user_name, course_id, amount, created_at, status
        FROM transactions
        ORDER BY created_at DESC
        LIMIT 10
    """)
    recent_transactions = cursor.fetchall()
    
    # AI agents status (simulated)
    ai_status = [
        {"name": "Marketing Agent", "status": "active", "status_color": "#4CAF50", 
         "icon": "fas fa-bullhorn", "description": "Promotes courses on social media",
         "uptime": 99.8, "tasks_completed": 124},
        {"name": "Support Agent", "status": "active", "status_color": "#4CAF50",
         "icon": "fas fa-headset", "description": "Handles customer inquiries 24/7",
         "uptime": 100, "tasks_completed": 87},
        {"name": "Content Agent", "status": "active", "status_color": "#4CAF50",
         "icon": "fas fa-file-alt", "description": "Creates new course content",
         "uptime": 98.5, "tasks_completed": 15},
        {"name": "Payment Agent", "status": "active", "status_color": "#4CAF50",
         "icon": "fas fa-credit-card", "description": "Processes transactions securely",
         "uptime": 99.9, "tasks_completed": 186}
    ]
    
    conn.close()
    
    return {
        "total_revenue": sum([r[1] for r in revenue_data]),
        "active_students": get_active_students(),
        "conversion_rate": calculate_conversion_rate(),
        "refund_rate": refund_rate,
        "revenue_data": revenue_data,
        "province_data": province_data,
        "course_data": course_data,
        "recent_transactions": recent_transactions,
        "ai_status": ai_status
    }

def save_dashboard_data():
    """Save dashboard data to JSON file"""
    data = generate_dashboard_data()
    with open('frontend/data/dashboard.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    save_dashboard_data()
