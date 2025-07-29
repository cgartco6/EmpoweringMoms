import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/support', methods=['POST'])
def handle_support():
    data = request.json
    user_message = data['message']
    
    # Simple AI response (in production, use OpenAI API)
    responses = {
        "payment": "Please visit https://payfast.co.za for payment issues",
        "access": "Course access is granted immediately after payment confirmation",
        "refund": "Refunds available within 14 days. Email refunds@yourdomain.com"
    }
    
    if "payment" in user_message.lower():
        return jsonify({"response": responses["payment"]})
    elif "access" in user_message.lower():
        return jsonify({"response": responses["access"]})
    elif "refund" in user_message.lower():
        return jsonify({"response": responses["refund"]})
    else:
        return jsonify({"response": "Please email support@yourdomain.com for further assistance"})

if __name__ == '__main__':
    app.run(port=5000)
