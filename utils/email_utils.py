# utils/email_utils.py
import smtplib
import random
import string
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    """Send OTP to user's email address."""
    try:
        # Email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        # Check if email credentials are configured
        if not sender_email or not sender_password:
            return False, "Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Mental Health AI Copilot - Password Reset OTP"
        
        # Email body
        body = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <h2 style="color: white; margin: 0;">🔐 Password Reset</h2>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                    <h3 style="color: #495057; margin-top: 0;">Your One-Time Password (OTP)</h3>
                    <p>Hello,</p>
                    <p>You requested a password reset for your Mental Health AI Copilot account.</p>
                    
                    <div style="background: white; padding: 20px; border-radius: 8px; text-align: center; 
                                border: 2px solid #667eea; margin: 20px 0;">
                        <h1 style="color: #667eea; font-size: 36px; margin: 0; letter-spacing: 5px;">{otp}</h1>
                    </div>
                    
                    <p><strong>Instructions:</strong></p>
                    <ol>
                        <li>Use this OTP as your temporary password to login</li>
                        <li>After logging in, go to your Profile page</li>
                        <li>Change your password to something secure</li>
                    </ol>
                    
                    <p style="color: #dc3545; font-weight: bold;">⚠️ This OTP is valid for 10 minutes only.</p>
                    <p style="color: #6c757d; font-size: 14px;">If you didn't request this password reset, please ignore this email.</p>
                </div>
                
                <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                    <p>Mental Health AI Copilot - Your Mental Wellness Companion</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        return True, "OTP sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
