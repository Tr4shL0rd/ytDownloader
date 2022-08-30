import re
import os
import sys
import json
from textwrap import indent
import dotenv
import youtube_dl
import datetime
import tkinter as tk
from inspect import currentframe
from rich.console import Console

########## GLOBALS ##########

home = os.path.expanduser("~")
urlsPath = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "urls.txt")
    )

downloadsPath = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", 
        "downloads")
    )

configPath = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", 
        "config.json")
    )

historyPath = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "history.json")
    )

dotenv.load_dotenv()

console = Console()

debugSongs = ["youtube-dl test video ''_ä↭𝕐.mp3"]


def getVersion():
    version = "0.5.0"
    console = Console()
    with console.capture():
        returnMessage = f"[bold yellow]VERSION: {version}[/bold yellow]"
    console.print(returnMessage)


########## TKINTER ##########

def deleteEntries(fields):
    fields.delete("1.0", tk.END)

########## YouTube-dl ##########


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def myHook(d: dict):
    if d['status'] == 'downloading':
        print\
        (f"Downloading \"{d['filename'].split('/')[-1]}\" [{d['_percent_str']}] [{d['_eta_str']}]", end='\r')
    if d['status'] == 'finished':
        print("" * 200, end="\r")
        print('\nDone downloading, now converting...')
        print(f"downloaded \"{d['filename'].split('/')[-1]}\" to downloads/\n")

# youtubeDL Options
ydlOpts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "extractaudio": True,
    "addmetadata": True,
    "writethumbnail": True,
    "logger": Logger(),
    "progress_hooks": [myHook],
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    },
        {"key": "FFmpegMetadata"},
        {"key": "EmbedThumbnail"},
    ],
}
########## STRING MANIPULATION ##########

def listToString(string:list):
    return "".join(string)

def usefullMetaData(url):
    returns = []
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        data = ydl.extract_info(url, download=False)
        returns.append(data["track"])
        returns.append(data["artist"])
        returns.append(data["thumbnail"])
        return returns


def fixSongNames(songs: list):
    blacklistWords = [
        "(official music video)",
        "(lyrics)",
        "(lyrics video)",
        "(official)",
        "(video)",
        "(music video)",
        "(official video)",
        "[Live at Improve Tone Studios, 2015]",
        "[HD]",
        "[Official Lyric Video]"
    ]
    
    lofiWords = [
        "lofi",
        "lo-fi",
    ]
        

    # remove blacklistWords and check if there are any empty [] after in song name and then remove them
    fixedSongNames = []
    #print(f"Original song names: {songs}")
    if type(songs) == list: 
        for song in songs:
            for lofi in lofiWords:
                if lofi in song.lower():
                    song += "{lofi}"
            song = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", song)
            song = song.replace("()", "").replace("[]", "")
            for word in blacklistWords:
                song = song.lower().replace(word, "").replace(" ", "_").replace("_.", ".").replace(
                    "_.", ".").replace("_", " ").replace("{", "[").replace("}", "]")
            fixedSongNames.append(song)
        return fixedSongNames
    elif type(songs) == str:
        for lofi in lofiWords:
            if lofi in songs.lower():
                songs += "{lofi}"
        songs = re.sub("[\(\[].*?[\)\]]", "", songs)
        songs = songs.replace("()", "").replace("[]", "")
        for word in blacklistWords:
            songs = songs.lower().replace(word, "").replace(" ", "_").replace("_.", ".").replace(
                "_.", ".").replace("_", " ").replace("{", "[").replace("}", "]")
        fixedSongNames.append(songs)
        return fixedSongNames[0]

def fixDownloadedSongNames() -> None:
    filenames = [filenames for filenames in os.listdir(downloadsPath) if os.path.isfile(os.path.join(downloadsPath, filenames))]
    fixedSongNames = [fixedSongNames for fixedSongNames in map(fixSongNames, filenames)]
    for filename in filenames:
        filePath = os.path.join(downloadsPath, filename)
        os.rename(filePath, os.path.join(downloadsPath, fixedSongNames[filenames.index(filename)]))

########## CHECKS ##########


def urlIsValid(url: str):
    regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    if re.search(regex, url):
        return True
    else:
        return False


def checkForCommentInUrlFile():
    with open(urlsPath, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                return True
            else:
                return False


def checkBadLURLS():
    with open(urlsPath, "r") as urlFile:
        lines = urlFile.readlines()
        for i, line in enumerate(lines):
            i += 1
            if "\n" in line:
                return i


def checkForConfigBlanks():
    with open("config.json", "r") as configFile:
        config = json.load(configFile)
        for key, value in config.items():
            if f"{key.upper()} BLANK!" == value:
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
    with open(urlsPath, "r") as urls:
        for url in urls.readlines():
            url = url.replace("\n", "")
            urlList.append(url)
    return urlList


def getAllDownloads():
    folder = []
    for _, _, files in os.walk(downloadsPath):
        for file in files:
            folder.append(file)
    return folder


def emptyDownloadsFolder(choice=True):
    for _, _, files in os.walk(downloadsPath):
        for file in files:
            if choice:
                os.remove(os.path.join(downloadsPath, file))


def removeEmptyLines():
    with open(urlsPath, "r") as urlFile:
        lines = urlFile.readlines()
    with open(urlsPath, "w") as urlFile:
        goodLines = []
        for line in lines:
            if line != "\n":
                goodLines.append(line)
        for gLine in goodLines:
            urlFile.write(gLine)


def emptyUrlFile():  # TODO: REFACTOR!!!!!!
    with open(urlsPath, "r") as f:
        lines = f.readlines()
    with open(urlsPath, "w") as f:
        for line in lines:
            if "#" in line:
                f.write(line.strip())
    with open(urlsPath, "r") as f:
        lines = f.readlines()

    with open(urlsPath, "r") as f:
        linesToWrite = []
        for line in lines:
            if "#" in line:
                linesToWrite.append(line.replace("#", "\n#"))
    with open(urlsPath, "w") as f:
        for line in linesToWrite:
            f.write(line)
    with open(urlsPath, "r") as f:
        lines = f.readlines()
    with open(urlsPath, "w") as f:
        moreLines = []
        for line in lines:
            if line != "\n":
                moreLines.append(line)
        f.write("".join(moreLines))


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


def getYoutubeTitle(url: str):
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(url, download=False)
    return result['title']


def getYoutubeId(url: str):
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(url, download=False)
    return result['id']


def getYoutubeKeys():
    keys = []
    with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
        result = ydl.extract_info(
            "https://www.youtube.com/watch?v=BaW_jenozKc", download=False)
    for key in result.keys():
        keys.append(key)
    return keys


def getYoutubeData(url: str, key: str):
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


def removePathFromString(string: str):
    return string.split("/")[-1]


def DEBUG_MESSAGE(iterator=0, additionalMessage=""):
    console = Console()
    with console.capture() as capture:
        returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]DEBUG MESSAGE #{iterator}[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}\nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
        if additionalMessage != "":
            returnMessage = f"[bold red]══════════════════════════\n[/bold red][bold yellow]DEBUG MESSAGE #{iterator}[/bold yellow] [cyan]|[/cyan] [bold yellow]{sys.argv[0]}[/bold yellow] [cyan]|[/cyan][bold yellow] {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}[/bold yellow]\n[bold red]══════════════════════════[/bold red]"
        console.print(returnMessage)
    return capture.get().strip()

def writeToHistory(url="", id="", title="", channel=""):
    with open(historyPath, "a") as history:
        dataFormat = {
            datetime.datetime.now().strftime("%d/%m/%y"): {
                "Time Downloaded": datetime.datetime.now().strftime("%H:%M"),
                "URL": url,
                "ID": id,
                "title": title,
                "Channel": channel,
            }
        }
        history.write(f",{json.dumps(dataFormat, indent=4)}")

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

########## COLORLESS WARNINGS ##########


def ncWARNING(additionalMessage=""):
    returnMessage = f"══════════════════════════\nWARNING | {sys.argv[0]} \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    if additionalMessage != "":
        returnMessage = f"══════════════════════════\nWARNING | {sys.argv[0]} | {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    print(returnMessage)


def ncINFO(additionalMessage=""):
    returnMessage = f"══════════════════════════\nINFO | {sys.argv[0]} \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    if additionalMessage != "":
        returnMessage = f"══════════════════════════\nINFO | {sys.argv[0]} | {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    print(returnMessage)


def nconelineInfo(Message=""):
    print(f"INFO | {Message}\n══════════════════════════\n")


def ncERROR(additionalMessage="", traceback=None):
    returnMessage = f"══════════════════════════\nERROR | {sys.argv[0]} \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    if additionalMessage != "":
        returnMessage = f"══════════════════════════\nERROR | {sys.argv[0]} | {additionalMessage}  \nON LINE:{currentframe().f_back.f_lineno}\n══════════════════════════"
    if traceback:
        returnMessage += f"\nTRACEBACK:\n{traceback}"
    print(returnMessage)
