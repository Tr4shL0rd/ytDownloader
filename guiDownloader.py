import os
import json
import signal
import tkinter as tk
from tkinter import StringVar, BooleanVar, IntVar, Variable, ttk
import tkinter.messagebox as messagebox
import guiDevTools.guiHelper as guiHelper
import devTools.helper as helper

# ROOT MANAGEMENT
root = tk.Tk()
root.geometry("500x200")
root.resizable(False, False)
root.title("YouTube Downloader")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='assets/icon/icon.ico'))
# FRAME MANAGEMENT
frame = tk.Frame(root)

# GRID MANAGEMENT
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# FONTS
labelFont = ("Helvetica", 12)


def dump(sender, reciever, password, url):
    print(sender, reciever, password, url)

class progress:
    progress_text = tk.Label(
        root,
        text=f"Progress: ",
        font=labelFont

    )

class download_Button():
    download_Button_icon = tk.PhotoImage(file="./assets/buttons/download.png")

    def download_Button_Clicked():
        messagebox.showinfo(
            title="Infomation",
            message=f"Downloading {url_Field.getUrl()}"
        )

    download_Button_Butt = ttk.Button(
        root,
        image=download_Button_icon,
        text="Download",
        compound=tk.LEFT,
        command=lambda: guiHelper.download(
            sender         = getEntrie.sender(),
            reciever       = getEntrie.reciever(),
            password       = getEntrie.password(),
            attachment     = getEntrie.url(),
            loadedFromFile = load_Url_File.loadFromFile.get()
        )
    )


class sender_Field:
    def __init__(self):
        pass
    sender_Field_Label = tk.Label(
        root,
        text="SENDER",
        font=labelFont
    )
    sender_Field_Text = tk.Entry(
        root,
    )


class reciever_Field:
    def __init__(self):
        pass

    reciever_Field_Label = tk.Label(
        root,
        text="RECIEVER",
        font=labelFont
    )
    reciever_Field_Text = tk.Entry(
        root,
    )


class password_Field:
    def __init__(self):
        pass

    password_Field_Label = tk.Label(
        root,
        text="PASSWORD",
        font=labelFont
    )
    password_Field_Text = tk.Entry(
        root,
        # show="*"
    )


class url_Field:
    def __init__(self):
        pass

    url_Field_Text_Label = tk.Label(
        root,
        text="YOUTUBE URL",
        font=labelFont
    )
    url = StringVar()
    url_Field_Text = tk.Entry(
        root,
        textvariable=url,
    )

    url_Field_Commit = tk.Button(
        root,
        text="Download",
    )


class load_Url_File:
    def __init__(self):
        pass
    urlCount = tk.Label(
                root,
                text=f"{len(helper.urlReader())} songs loaded",
                font=labelFont
            )
    def loadFromUrlClicked():
        if load_Url_File.loadFromFile.get():
            
            load_Url_File.urlCount.grid(row=2, column=1, sticky=tk.W)
            url_Field.url_Field_Text_Label.grid_remove()
            url_Field.url_Field_Text.grid_remove()
        else:
            load_Url_File.urlCount.grid_remove()
            url_Field.url_Field_Text_Label.grid(column=1, row=2, sticky=tk.W)
            url_Field.url_Field_Text.grid(column=1, row=3, sticky=tk.W)
    loadFromFile = BooleanVar()
    load_Url_File_Button = tk.Checkbutton(
        root,
        text="Load from file",
        variable=loadFromFile,
        command=lambda: load_Url_File.loadFromUrlClicked()
    )


class remeber_Me:
    def __init__(self):
        pass

    def saveCreds():
        if remeber_Me.remeber.get():
            guiHelper.saveToConfig(
                senderName=    getEntrie.sender(),
                reciever=      getEntrie.reciever(),
                senderPassword=getEntrie.password()
            )
    remeber = BooleanVar()
    remeber_Me_Button = tk.Checkbutton(
        root,
        text="Remember Me",
        variable=remeber,
        command=lambda: guiHelper.saveToConfig(
            senderName=    getEntrie.sender(),
            reciever=      getEntrie.reciever(),
            senderPassword=getEntrie.password()
        )
    )


class general:
    def __init__(self):
        pass

    dumpButton = tk.Button(
        root,
        text="DEBUG"
    )


sender_Field.sender_Field_Label.grid(column=0, row=0, sticky=tk.W)
sender_Field.sender_Field_Text.grid(column=0, row=1, sticky=tk.W)
sender_Field.sender_Field_Text.insert(
    0, json.loads(open("config.json").read())["username"])

reciever_Field.reciever_Field_Label.grid(column=1, row=0, sticky=tk.W)
reciever_Field.reciever_Field_Text.grid(column=1, row=1, sticky=tk.W)
reciever_Field.reciever_Field_Text.insert(
    0, json.loads(open("config.json").read())["receiver"])

password_Field.password_Field_Label.grid(column=2, row=0, sticky=tk.W)
password_Field.password_Field_Text.grid(column=2, row=1, sticky=tk.W)
password_Field.password_Field_Text.insert(
    0, json.loads(open("config.json").read())["password"])

url_Field.url_Field_Text_Label.grid(column=1, row=2, sticky=tk.W)
url_Field.url_Field_Text.grid(column=1, row=3, sticky=tk.W)

download_Button.download_Button_Butt.grid(column=1, row=4, sticky=tk.W, padx=5)
load_Url_File.load_Url_File_Button.grid(column=1, row=5, sticky=tk.W)
remeber_Me.remeber_Me_Button.grid(column=1, row=6, sticky=tk.W)
#progress.progress_text.grid(column=1, row=7, sticky=tk.W)

class getEntrie():
    def url():
        return url_Field.url_Field_Text.get()

    def sender():
        return sender_Field.sender_Field_Text.get()

    def reciever():
        return reciever_Field.reciever_Field_Text.get()

    def password():
        return password_Field.password_Field_Text.get()


def getRadioButtonValue():
    return load_Url_File.load_Url_File_Button.get()


try:
    root.mainloop()
except KeyboardInterrupt:
    os.kill(os.getpgid(0), signal.SIGTERM)
