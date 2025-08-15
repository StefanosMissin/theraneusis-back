import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_verification_email(email: str, token: str):
    link = f"https://theraneusis.com/auth/login?token={token}&email={email}"

    # HTML email with a button
    html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="text-align: center;">Καλώς ήρθατε στο THERANEUSIS!</h2>
            <p style="text-align: center; margin: 15px auto;">
            Σας ευχαριστούμε για την εγγραφή σας. Παρακαλούμε πατήστε το παρακάτω κουμπί για να επαληθεύσετε τον λογαριασμό σας:
            </p>
            <p style="text-align: center;">
            <a href="{link}"
                style="background-color: #4CAF50; color: white; padding: 12px 20px; 
                        text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block; margin-top: 15px; margin-bottom: 15px;">
                Επαλήθευση Λογαριασμού
            </a>
            </p>
            <p style="text-align: center; margin: 15px auto;">
            Αν το κουμπί δεν λειτουργεί, αντιγράψτε και επικολλήστε τον παρακάτω σύνδεσμο στον περιηγητή σας:
            </p>
            <p style="text-align: center; margin: 15px auto;">
            <a href="{link}">{link}</a>
            </p>
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
            <h2 style="text-align: center;">Επαναφορά Κωδικού Πρόσβασης</h2>
            <p style="text-align: center; margin: 15px auto;">Γεια σου {first_name},</p>
            <p style="text-align: center; margin: 15px auto;">
            Λάβαμε αίτημα για επαναφορά του κωδικού πρόσβασής σας. Κάντε κλικ στο παρακάτω κουμπί για να ορίσετε νέο κωδικό:
            </p>
            <p style="text-align: center;">
            <a href="{link}"
                style="background-color: #1A5362; color: white; padding: 12px 20px;
                        text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block; margin-top: 15px; margin-bottom: 15px;">
                Επαναφορά Κωδικού
            </a>
            </p>
            <p style="text-align: center; margin: 15px auto;">
            Αυτός ο σύνδεσμος θα λήξει σε 24 ώρες. Αν δεν κάνατε εσείς το αίτημα, μπορείτε απλώς να αγνοήσετε αυτό το email.
            </p>
            <p style="text-align: center; margin: 15px auto;">
            Αν το κουμπί δεν λειτουργεί, αντιγράψτε και επικολλήστε τον παρακάτω σύνδεσμο στον περιηγητή σας:
            </p>
            <p style="text-align: center; margin: 15px auto;">
            <a href="{link}">{link}</a>
            </p>
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