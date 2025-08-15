import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_verification_email(email: str, token: str):
    link = f"https://theraneusis.com/auth/login?token={token}&email={email}"

    # HTML email with a button
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="text-align: center;">Welcome to THERANEUSIS!</h2>
            <p style="text-align: center; margin: 15px auto;">Thank you for registering. Please click the button below to verify your account:</p>
            <p style="text-align: center;">
                <a href="{link}" 
                   style="background-color: #4CAF50; color: white; padding: 12px 20px; 
                          text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block; marin-top: 15px; maring-bottom: 15px;">
                    Verify My Account
                </a>
            </p>
            <p style="text-align: center; margin: 15px auto;">If the button doesn't work, copy and paste the following link into your browser:</p>
            <p style="text-align: center; margin: 15px auto;"><a href="{link}">{link}</a></p>
        </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = "THERANEUSIS - Verify your account"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)


def send_password_reset_email(email: str, first_name: str, token: str):
    link = f"https://theraneusis.com/auth/lost-password/reset?token={token}"

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="text-align: center;">Reset Your Password</h2>
            <p style="text-align: center; margin: 15px auto;">Hello {first_name},</p>
            <p style="text-align: center; margin: 15px auto;">
                We received a request to reset your password. Click the button below to choose a new one:
            </p>
            <p style="text-align: center;">
                <a href="{link}" 
                   style="background-color: #1A5362; color: white; padding: 12px 20px; 
                          text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block; margin-top: 15px; margin-bottom: 15px;">
                    Reset My Password
                </a>
            </p>
            <p style="text-align: center; margin: 15px auto;">
                This link will expire in 24 hours. If you did not request this, you can safely ignore this email.
            </p>
            <p style="text-align: center; margin: 15px auto;">If the button doesn't work, copy and paste the following link into your browser:</p>
            <p style="text-align: center; margin: 15px auto;"><a href="{link}">{link}</a></p>
        </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = "THERANEUSIS - Reset your password"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)