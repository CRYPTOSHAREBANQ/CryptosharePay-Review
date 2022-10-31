import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailClient:
    def __init__(self) -> None:
        # self.host = "email-smtp.us-east-1.amazonaws.com"
        # self.sender = "no-reply@cryptosharepay.com"
        # self.username = "AKIA2GA5YBIERCRQY6HA"
        # self.password = "BP78z4AeWgcFI89WYoO8Wdcz2FA8suGBNWEqjLk3GVEh"

        # self.port = 2587

        self.host = "mail.cryptoshareapp.com"
        self.sender = "no-reply@cryptoshareapp.com"
        self.username = "no-reply@cryptoshareapp.com"
        self.password = "KkingCRYPTO$$21"

        self.port = 587

    def send_html_email(self, subject, content, to_address):

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"CryptosharePay - {subject}"
        msg['From'] = f"Crypto$harepay <{self.sender}>"
        msg['To'] = to_address

        email_content = MIMEText(content, 'html')

        msg.attach(email_content)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.host,self.port) as smtp_server:
                smtp_server = smtplib.SMTP(self.host,self.port)
                smtp_server.ehlo()
                smtp_server.starttls(context=context)
                smtp_server.ehlo()
                smtp_server.login(self.username, self.password)
                smtp_server.sendmail(self.sender, to_address, msg.as_string())
        except Exception as error:
            print(error)
        
        return

    
    def complete_transaction(self, transaction):

        subject = f"Transaction {transaction.transaction_id} completed"

        content = f"""
        <html>
            <body>
                <h1> Hi there! </h1>

                <p> You are receiving this email because a transaction has been <b>completed.</b> </p>

                <p> Details of the transaction as follows: </p>

                <p> Transaction ID: {transaction.transaction_id} </p>

                <p> Transaction description: {transaction.description} </p>

                <p> Transaction type: {transaction.type} </p>
                
                <p>
                    For further information, please make make use of API endpoint using your API key.

                    https://api.cryptosharepay.com/v1/transactions/payments/{transaction.transaction_id}/

                </p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, str(transaction.api_key.user_id.email))

    def cancel_transaction(self, transaction):
        subject = f"Transaction {transaction.transaction_id} cancelled"

        content = f"""
        <html>
            <body>
                <h1> Hi there! </h1>

                <p> You are receiving this email because a transaction has been <b>cancelled.</b> </p>

                <p> Details of the transaction as follows: </p>

                <p> Transaction ID: {transaction.transaction_id} </p>

                <p> Transaction description: {transaction.description} </p>

                <p> Transaction type: {transaction.type} </p>
                
                <p>
                    For further information, please make make use of API endpoint using your API key.

                    https://api.cryptosharepay.com/v1/transactions/payments/{transaction.transaction_id}/

                </p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, str(transaction.api_key.user_id.email))




