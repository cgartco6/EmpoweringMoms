import os
import random
import requests
from flask import Flask, request, jsonify
from utils import get_config, generate_ai_response

app = Flask(__name__)

SUPPORT_CONTEXT = """
You are Sarah, a customer support agent for Empowering Moms. 
You're speaking with South African mothers who want financial freedom.
Be empathetic, helpful, and solution-oriented. Use simple language.
"""

@app.route('/support', methods=['POST'])
def handle_support():
    data = request.json
    user_message = data['message']
    user_info = data.get('user', {})
    
    # Generate human-like response
    prompt = f"{SUPPORT_CONTEXT}\n\nUser: {user_message}\n\nSarah:"
    response = generate_ai_response(prompt, max_tokens=200)
    
    # Handle specific cases
    if "refund" in user_message.lower():
        response = handle_refund_request(user_info)
    elif "payment" in user_message.lower():
        response = handle_payment_issue(user_info)
    
    return jsonify({"response": response, "agent": "Sarah"})

def handle_refund_request(user):
    """Process refund requests"""
    # Check user's purchase history
    # Generate refund policy explanation
    prompt = f"{SUPPORT_CONTEXT} Explain our refund policy to a user who requested a refund"
    return generate_ai_response(prompt)

def handle_payment_issue(user):
    """Resolve payment issues"""
    prompt = f"{SUPPORT_CONTEXT} Help a user resolve a payment issue"
    return generate_ai_response(prompt)

if __name__ == '__main__':
    app.run(port=5000)
