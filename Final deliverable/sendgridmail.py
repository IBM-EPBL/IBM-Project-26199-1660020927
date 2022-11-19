#import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendmail(usermail,subject,content):
    message = Mail(from_email='harshinisivakami@student.tce.edu',to_emails=usermail,subject=subject,html_content='<strong> {} </strong>'.format(content))
    try:
        sg = SendGridAPIClient(os.environ.get(['SENDGRID_API_KEY'])
       
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
        
        
