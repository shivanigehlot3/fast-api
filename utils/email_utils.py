import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_reset_email(to_email, token):
    subject = "Password Reset Request"

    plain_text_body = f"""
    Hello,

    You requested a password reset.

    Your password reset token is: {token}

    This token is valid for 30 minutes.

    If you did not request this, please ignore this email.

    Thank you,
    E-Commerce System
    """

    html_body = f"""
    <html>
    <head>
        <style>
            .container {{
                font-family: Arial, sans-serif;
                padding: 20px;
                color: #333333;
                background-color: #f9f9f9;
                border-radius: 10px;
                max-width: 600px;
                margin: auto;
                border: 1px solid #e0e0e0;
            }}
            .header {{
                font-size: 24px;
                font-weight: bold;
                color: #2e6da4;
                margin-bottom: 20px;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.5;
            }}
            .token {{
                font-size: 20px;
                font-weight: bold;
                background-color: #f0f0f0;
                padding: 10px;
                display: inline-block;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Password Reset Request</div>
            <div class="content">
                <p>Hello,</p>
                <p>You requested to reset your password.</p>
                <p>Your password reset token is:</p>
                <div class="token">{token}</div>
                <p>This token is valid for 30 minutes.</p>
                <p>If you did not request this, please ignore this email.</p>
                <p>Thank you,<br>
                E-Commerce System</p>
            </div>
            <div class="footer">
                &copy; 2025 E-Commerce System. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative") 
    msg["From"] = settings.EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(plain_text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[INFO] Reset email sent to {to_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {to_email}: {e}")
