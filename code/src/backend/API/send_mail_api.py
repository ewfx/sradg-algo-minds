import pandas as pd
import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, jsonify

send_mail_bp = Blueprint('send_mail_bp', __name__)

# Sample DataFrame
data = {
    'Match Type': ['match', 'break', 'break', 'match'],
    'Anomaly Type': ['None', 'Mismatch Amount', 'Missing Entry', 'None']
}
df = pd.DataFrame(data)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Change this if using a different mail service
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

@send_mail_bp.route('/send-mail', methods=['POST'])
def send_mail():
    global df
    anomalies = df[df['Match Type'] == 'break']['Anomaly Type'].tolist()

    if not anomalies:
        return jsonify({"message": "No anomalies found to report"}), 200

    email_body = "Dear User,\n\nThe following anomalies were found during reconciliation:\n\n"
    email_body += "\n".join([f"- {anomaly}" for anomaly in anomalies])
    email_body += "\n\nBest Regards,\nYour System"

    response = send_email("palashbajpai45@gmail.com", "Anomaly Report", email_body)
    return jsonify({"message": response})
