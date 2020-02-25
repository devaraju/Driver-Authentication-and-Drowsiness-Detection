import os
import getpass
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from combined_image import getCombinedImage

def sendAlertMail():
    print("[INFO] Preparing alert mail template.")
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL

    sender_email = input("Enter sender mail: ")
    receiver_email = input("Enter reciever mail: ")

    #message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Alert from Driver Authentication System"
    message["From"] = sender_email
    message["To"] = receiver_email

    #create plain and HTML version of message
    text = """\
        Hi there,
        This is an alert mail from Driver Authentication System that someone trying to acess your vechicle.
        """

    html = """\
        <html>
            <body>
                <p>Hi there,<br>
                <h2 style="color:red">This is an alert mail from Driver Authentication System that someone trying to access your vechicle.</h2>
                <span style="color:gray;font-size:14px">The attached image contains anonymous person's facial data.</spam>
                </p>
            </body>
        </html>
    """
    try:
        imageName = getCombinedImage()
    except:
        basePath = os.getcwd()
        imageName = os.path.join(basePath, "anonymous images", "anonymous.png")

    image = open(str(imageName), 'rb').read()        
    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    image_part = MIMEImage(image, name=os.path.basename(imageName)) 

    message.attach(text_part)
    message.attach(html_part)
    message.attach(image_part)

    # Create a secure SSL context
    context = ssl.create_default_context()
    try: 
        password = getpass.getpass('Enter email password: ') 
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print(f'[Success] An alert mail sent to {receiver_email}')
    except:
        print("[Error] Something went wrong.")

if __name__ == "__main__":
    sendAlertMail()