import smtplib
import uuid
from email.message import EmailMessage

key = uuid.uuid4()
msg = EmailMessage()
msg.set_content("Authentication token\n%s\n" % key)

msg['Subject'] = 'Trusted Capsule Registration request'
msg['From'] = "eric.semeniuc@gmail.com"
msg['To'] = "eric.semeniuc@gmail.com"

gmail_user = 'bobthehaxor@gmail.com'
gmail_password = ''
try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.login(gmail_user, gmail_password)
    server_ssl.send_message(msg)
    server_ssl.quit()
except:
    print('Something went wrong...')
