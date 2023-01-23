from fileinput import filename
import sys
import smtplib
import datetime
from flask import *
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/mail/send', methods=['POST'])
def sendemail():

    #SMTP details
    server = smtplib.SMTP('relay.xyz.com', 25)
    server.ehlo()
    server.starttls()

    #Set defaults
    from_address = 'donotreply@xyz.com'

    #Request parameters
    subject = request.form['subject']
    message_body = request.form['messagebody']
    to_address = request.form['toaddress']
    from_address = request.form['fromaddress']
    filename = request.form['filename']
    attachment = request.files.get('attachment', '').read()

    #msg = str(datetime.datetime.now()) + ': ' + subject + '\r\n' + message_body

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = from_address
    message["To"] = to_address
    message["Subject"] = subject
    message["Bcc"] = to_address  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(message_body, "plain"))

    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment)

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    print("################")
    print(text)
    print("################")

    try:
        server.sendmail(from_address, to_address, text)
        data = {
            'status' : "Mail Sending SUCCESS",
            'message' : text
            }
        print("Mail Sending SUCCESS")
    except:
        print("Error : ", sys.exc_info())
        data = {
            'status' : "Mail Sending FAILED",
            'message' : text
            }
        print("Mail Sending FAILED")
    finally:
        server.quit()
    
    json_dump = json.dumps(data)
    return json_dump

def notifyme(subjStr, msgStr, sendToEmailToo=False):
    server = smtplib.SMTP('relay.xyz.com', 25)
    server.ehlo()
    server.starttls()

    from_address = 'donotreply@xyz.com'
    if(sendToEmailToo):
        to_address = "firstName.LastName@xyz.com"
    else:
        to_address = ['<PhoneNumber_Deleted>@txt.att.net']

    msg = str(datetime.datetime.now()) + ': ' + subjStr + '\r\n' + msgStr

    try:
        server.sendmail(from_address, to_address, msg)
        print('Status Sending Success')
        print('*****************')
        print(msg)
        print('*****************')
    except:
        print('FAILURE: Status Sending FAILED')
        print('*****************')
        print(msg)
        print('*****************')
    server.quit()

def main():
    notifyme("Test", "Test body", True)
    

if __name__ == "__main__":
    main()
    

if __name__ == "__main__":
    app.run(port=7777)
