import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import dotenv_values


config = dotenv_values(".env")

def send_email(subject, body, recipient_email):
    # Your email credentials
    sender_email = config["SENDER_EMAIL"]
    sender_password = config["SENDER_PASSWORD"]

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.zoznam.sk', 587)
        # server.starttls()  # Use TLS
        
        # Log in to your email account
        server.login(sender_email, sender_password)
        
        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")
    
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    finally:
        # Close the server connection
        server.quit()
