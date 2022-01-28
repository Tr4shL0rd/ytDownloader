import json


class mail():
    def senderName():
        username = input("Your Gmail Username: ")
        if username != "":
            return username
        else:
            return "USERNAME BLANK!"
        
    def senderPassword():
        password = input("Your gmail password: ")
        if password != "":
            return password
        else:
            return "PASSWORD BLANK!"

    def receiverMail():
        receiver = input("Reciever email: ")
        if receiver != "":
            return receiver
        else:
            return "RECEIVER BLANK!"


def saveToConfig(senderName, senderPassword, reciever):    
    with open("config.json", "w") as configFile:
        json.dump(
            {
                "username": senderName, 
                "password": senderPassword, 
                "receiver": reciever, 
                "written": True
            }, 
            configFile
        )

try:
    name = mail.senderName()
    password = mail.senderPassword()
    reciever = mail.receiverMail()

    if "BLANK!" in name or "BLANK!" in password or "BLANK!" in reciever:
        print("One of the fields is blank!")
        choice = input("Are you sure you want to continue?(y/N): ") or "N"
        if choice.lower() == "y":
            saveToConfig(name,password,reciever)
        else:
            exit()
    else:
        saveToConfig(name,password,reciever)
except KeyboardInterrupt:
    print("\nExting...")