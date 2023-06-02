import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailClient:
    def __init__(self) -> None:
        self.host = "email-smtp.us-east-1.amazonaws.com"
        self.sender = "no-reply@cryptosharepay.com"
        self.username = "AKIA2GA5YBIERCRQY6HA"
        self.password = "BP78z4AeWgcFI89WYoO8Wdcz2FA8suGBNWEqjLk3GVEh"

        self.port = 2587

        # self.host = "mail.cryptoshareapp.com"
        # self.sender = "no-reply@cryptoshareapp.com"
        # self.username = "no-reply@cryptoshareapp.com"
        # self.password = "KkingCRYPTO$$21"

        # self.port = 587

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

    
    def complete_transaction(self, transaction, email):

        subject = f"Transaction {transaction.transaction_id} completed"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

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

        self.send_html_email(subject, content, email)

    def cancel_transaction(self, transaction, email):
        subject = f"Transaction {transaction.transaction_id} cancelled"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

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

        self.send_html_email(subject, content, email)

    def cancel_automated_transaction(self, transaction, email):
        subject = f"Transaction {transaction.transaction_id} cancelled"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

                <p> You are receiving this email because a automated transaction has been <b>cancelled.</b> </p>

                <p> Details of the transaction as follows: </p>

                <p> Transaction ID: {transaction.transaction_id} </p>

                <p> Transaction description: {transaction.description} </p>

                <p> Transaction type: {transaction.type} </p>
                
                <p>
                    For further information, please contact support.
                </p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, email)

    def request_customer_id(self, security_pin, email):
        subject = f"Customer ID request"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

                <p> You are receiving this email because you requested your account Customer-Id </p>

                <em><p> Please do not share this information with anyone. </p><em>

                <p> Your security PIN is: </p>

                <h1> {security_pin} </h1>
                
                <p>
                    If you didn't request this information, please secure your account immediately.
                </p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, email)

    def cancel_expired_transaction(self, transaction, email):
        subject = f"Transaction {transaction.transaction_id} cancelled"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

                <p> You are receiving this email because your transaction {transaction.transaction_id} has expired therefore it has been cancelled</p>

                <p> Details of the transaction as follows: </p>

                <p> Transaction ID: {transaction.transaction_id} </p>

                <p> Transaction description: {transaction.description} </p>

                <p> Transaction type: {transaction.type} </p>
                
                <p>
                    Please remember transactions are only valid for 24 hours, after which they expire.
                </p>

                <p> If you still wish to complete this transaction, please create a new one via our API.</p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, email)

    def request_dashboard_login(self, random_password, email):
        subject = f"Dashboard Login request"

        content = f"""
        <html>
            <body>
                <h3> Hi there! </h3>

                <p> You are receiving this email because you requested to login into Cryptoshare Pay </p>

                <em><p> Please do not share this information with anyone. </p><em>

                <p> Your one-time randomized password is: </p>

                <h1> {random_password} </h1>
                
                <p>
                    If you didn't request this information, please secure your account immediately.
                </p>
            </body>
        </html>
        """

        self.send_html_email(subject, content, email)