import smtplib
from email.message import EmailMessage


def send_nonce(recipient_email: str, nonce: str) -> bool:
    msg = EmailMessage()
    msg.set_content("A device has requested registration"
                    "Please send the authentication token via verification command"
                    "Token:\n%s\n" % nonce)

    msg['Subject'] = 'Trusted Capsule Registration request'
    msg['From'] = "nsstester@gmail.com"
    msg['To'] = recipient_email

    gmail_user = 'YOUR_EMAIL@gmail.com'
    gmail_password = 'YOUR_PASSWORD'
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.login(gmail_user, gmail_password)
        server_ssl.send_message(msg)
        server_ssl.quit()
        return True
    except Exception as e:
        print(e)
        return False


def send_invite(recipient_email: str) -> bool:
    msg = EmailMessage()
    msg.set_content("A capsule has been authorized to this email"
                    "Please register via registration command")

    msg['Subject'] = 'Trusted Capsule Registration Invitation'
    msg['From'] = "nsstester@gmail.com"
    msg['To'] = recipient_email

    gmail_user = 'YOUR_EMAIL@gmail.com'
    gmail_password = 'YOUR_PASSWORD'
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.login(gmail_user, gmail_password)
        server_ssl.send_message(msg)
        server_ssl.quit()
        return True
    except Exception as e:
        print(e)
        return False
