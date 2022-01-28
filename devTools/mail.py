import smtplib
import mimetypes
from email.message import EmailMessage
from rich.console import Console 


def send(sender:str, password:str, receiver:str, attachment, subject="Title", body="Body", debug=False):
    attachmentName = f"{attachment}"

    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    message.set_content(body)
    mime_type, _ = mimetypes.guess_type(attachment)
    mime_type, mime_subtype = mime_type.split('/')
    with open(attachmentName, 'rb') as file:
        message.add_attachment(file.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment.split('/')[-1])
    
    
    Console().print("[bold green]Email sent![/bold green]")
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    if debug == True:
        mail_server.set_debuglevel(1)
    mail_server.login(sender, password)
    mail_server.send_message(message)
    mail_server.quit()


