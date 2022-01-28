import os
import sys
import json
import dotenv
import youtube_dl
import colorama

from inspect import currentframe
from rich.console import Console 

########## GLOBALS ##########

home = os.path.expanduser("~")
urlsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "urls.txt"))
downloadsPath  = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "downloads"))

########## LOGGING ##########

class Logger(object):
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
def myHook(d:dict):
    if d['status'] == 'finished':
        print("" * 200, end="\r")
        print('\nDone downloading, now converting ...')
        print(f"downloaded \"{d['filename'].split('/')[-1]}\" to downloads/")
    if d['status'] == 'downloading':
        print(f"Downloading \"{d['filename'].split('/')[-1]}\" [{d['_percent_str']}] [{d['_eta_str']}]", end='\r')
    
########## CHECKS ##########

def checkForCommentInUrlFile():
    with open(urlsPath, "r") as urls:
        for i,line in enumerate(urls.readlines()):
            if line.startswith("#"):
                return f"Comment found in line {i+1} of urls.txt"
    return False

def checkBadLURLS():
    #"/youtubeDownloader/devTools/urls.txt"
    with open(urlsPath, "r") as urlFile:
        lines = urlFile.readlines()
        for i,line in enumerate(lines):
            i += 1
            if "\n" in line:
                return i # i == badline

def checkForConfigBlanks():
    with open("config.json", "r") as configFile:
        config = json.load(configFile)
        for key, value in config.items():
            if f"{key.upper()} BLANK!" == value:
                #print(f"{key.upper()} is blank")
                return True
    return False

def checkIfConfigEmpty() -> bool:
    with open("config.json", "r") as configFile:
        try:
            json.load(configFile)
        except json.decoder.JSONDecodeError:
            return True
    return False
########## OS, FILES, SYSTEM ##########
def urlReader() -> list:
    urlList = []
    #/youtubeDownloader/devTools/urls.txt"
    with open(urlsPath, "r") as urls:
        for url in urls.readlines():
            url = url.replace("\n", "")
            urlList.append(url)
    return urlList

def getAllDownloads():
    #path = "/youtubeDownloader/downloads"
    folder = []
    #print("hje")
    for _,_, files in os.walk(downloadsPath):
        for file in files:
            folder.append(file)
    return folder

def emptyDownloadsFolder(choice=True):
    #path = "/youtubeDownloader/downloads/"
    for _, _,files in os.walk(downloadsPath):
        for file in files:
            if choice == True:
                os.remove(os.path.join(downloadsPath,file))
            
def removeEmptyLines():
    #reads the file
    #"/youtubeDownloader/devTools/urls.txt"
    with open(urlsPath, "r") as urlFile:
        lines = urlFile.readlines()
    #remove newline characters from file
    with open(urlsPath, "w") as urlFile:
        goodLines = []
        for line in lines:
            if line != "\n":
                goodLines.append(line)
        for gLine in goodLines:
            urlFile.write(gLine)

def emptyURLfile():
    with open(urlsPath, "w") as urlFile:
        urlFile.write("")
        
def getPassword():
    dotenv.load_dotenv()
    return os.getenv("PASSWORD")

def getSender():
    dotenv.load_dotenv()
    return os.getenv("sender")

def getReceiver():
    dotenv.load_dotenv()
    return os.getenv("reciever")

########## YOUTUBE_DL ##########

def getYoutubeTitle(url:str):
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(url, download=False)
    return result['title']

def getYoutubeId(url:str):
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(url, download=False)
    return result['id']

def getYoutubeKeys():
    keys = []
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info("https://www.youtube.com/watch?v=BaW_jenozKc", download=False)
    for key in result.keys():
        keys.append(key)
    return keys

def getYoutubeData(url:str, key:str):
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(url, download=False)
    return result[key]


########## MISC ##########

def getPaths():
    print(f"{home = }")
    print(f"{urlsPath = }")
    print(f"{downloadsPath = }")

def getConfig():
    with open("config.json", "r") as configFile:
        config = json.load(configFile)
        return config

def isDebug() -> bool:
    dotenv.load_dotenv()
    if os.getenv("DEBUG") == "TRUE":
        return True
    else:
        return False
def removePathFromString(string:str):
    return string.split("/")[-1]

def DEBUG_MESSAGE(iterator=0, additionalMessage=""):
    console = Console()
    with console.capture() as capture:
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]DEBUG MESSAGE #{iterator}[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}\nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
        if additionalMessage != "":
            returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]DEBUG MESSAGE #{iterator}[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow] {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
        console.print(returnMessage)
    return capture.get().strip()


########## WARNINGS ##########

def WARNING(additionalMessage=""):
    console = Console()
    with console.capture():
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]WARNING[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow]\nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    if additionalMessage != "":
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]WARNING[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow] {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    console.print(returnMessage)

def INFO(additionalMessage=""):
    console = Console()
    with console.capture():
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][blue]INFO[/blue] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow]\nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    if additionalMessage != "":
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][blue]INFO[/blue] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow] {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    console.print(returnMessage)

def onelineInfo(Message=""):
    console = Console()
    with console.capture():
        returnMessage = f"[blue]INFO[/blue] [cyan]|[/cyan] [bold yellow]{Message}[/bold yellow]\n[bold red]══════════════════════════\n[/bold red]"
    console.print(returnMessage)

def ERROR(additionalMessage="", traceback=None):
    console = Console()
    with console.capture():
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold red]ERROR[/bold red] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow]\nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    if additionalMessage != "":
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold red]ERROR[/bold red] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow] {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
    if traceback:
        returnMessage += f"\n[bold red]TRACEBACK:\n[/bold red]{traceback}"
    console.print(returnMessage)
