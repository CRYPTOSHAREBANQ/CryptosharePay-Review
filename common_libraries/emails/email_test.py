import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def test_email():
    host = "email-smtp.us-east-1.amazonaws.com"
    sender = "no-reply@cryptosharepay.com"
    username = "AKIA2GA5YBIERCRQY6HA"
    password = "BP78z4AeWgcFI89WYoO8Wdcz2FA8suGBNWEqjLk3GVEh"
    to = "albertonavarreteramirez@gmail.com"

    port = 2587
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Cryptosharepay test email"
    msg['From'] = f"Crypto$harepay <{sender}>"
    msg['To'] = to



    html = "<b> Test 2</b>"

    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    context = ssl.create_default_context()
    s = smtplib.SMTP(host,port)
    s.starttls(context=context)
    s.ehlo()
    s.login(username, password)
    s.sendmail(sender, to, msg.as_string())
    s.quit()
    return


test_email()