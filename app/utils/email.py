from flask import current_app, render_template
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        try:
            # Get configuration from environment variables or use defaults
            smtp_server = os.environ.get('MAIL_SERVER', 'smtp.example.com')
            smtp_port = int(os.environ.get('MAIL_PORT', 587))
            smtp_username = os.environ.get('MAIL_USERNAME', 'test@example.com')
            smtp_password = os.environ.get('MAIL_PASSWORD', 'password')
            smtp_use_tls = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', 'yes', '1')
            
            # Connect to SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()
            
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            # Log the error in a real application
            print(f"Failed to send email: {e}")
            return False

def send_email(subject, sender, recipients, text_body, html_body):
    """Create and send an email."""
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    
    # Add body parts
    text_part = MIMEText(text_body, 'plain')
    html_part = MIMEText(html_body, 'html')
    
    msg.attach(text_part)
    msg.attach(html_part)
    
    # Send email asynchronously
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    """Send password reset email to user."""
    # In production, use proper URL construction
    token = user.reset_token
    reset_url = f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/auth/reset-password/{token}"
    
    send_email(
        subject='QR Code Generator - Password Reset',
        sender=os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@qrcodegenerator.com'),
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, reset_url=reset_url),
        html_body=render_template('email/reset_password.html', user=user, reset_url=reset_url)
    ) 