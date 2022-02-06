import configparser
import json
import os.path
import smtplib
import mimetypes
import youtube_dl
import tkinter as tk
import devTools.mail as mail
import devTools.helper as helper
from email.message import EmailMessage



def deleteEntries(fields):
    fields.delete("1.0", tk.END)

def saveToConfig(senderName, senderPassword, reciever):   
    configPath = os.path.join(os.path.dirname(__file__), "..","config.json")
    with open(configPath, "w") as configFile:
        json.dump(
            {
                "username": senderName, 
                "password": senderPassword, 
                "receiver": reciever, 
                "written":  True
            }, 
            configFile
        )

ydlOpts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "extractaudio": True,
        "addmetadata": True,
        "writethumbnail": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
    }

def install(url):
    
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        ydl.download([url])
    

def download(sender, reciever, password, attachment):
    try:
        install(attachment)
        filename = helper.getAllDownloads()[0]
        send(sender, password, reciever, attachment=f"downloads/{filename}", subject=filename, body=filename)
    except smtplib.SMTPRecipientsRefused as e:
        print(e)
    except smtplib.SMTPAuthenticationError as e:
        print(e)



def send(sender:str, password:str, receiver:str, attachment, subject="Title", body="Body", debug=False):
    print(attachment)
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    message.set_content(body)
    mime_type, _ = mimetypes.guess_type(attachment)
    mime_type, mime_subtype = mime_type.split('/')
    with open(f"{attachment}", 'rb') as file:
        message.add_attachment(file.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment.split('/')[-1])
    
    
    #helper.emptyDownloadsFolder()
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    if debug:
        mail_server.set_debuglevel(1)
    mail_server.login(sender, password)
    mail_server.send_message(message)
    mail_server.quit()
    print("Email sent!")



