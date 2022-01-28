#!/usr/bin/env python3
import smtplib
import youtube_dl
import devTools.helper as helper
import devTools.mail as mail
import json
import devTools.downloaderArgs as downloaderArgs

# TODO: --no-color
# TODO: --no-download
# TODO: --json

# todo stderr for errors
# todo grep-able output

args = downloaderArgs.parser.parse_args()
if args.ignore == True:
    helper.INFO("Ignoring errors")



def install():
    ydlOpts = {
        'format': 'bestaudio/best',
        "outtmpl": "downloads/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        "logger": helper.Logger(),
        "progress_hooks": [helper.myHook],
    }
    url = helper.urlReader()
    
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        if args.no_download:
            for urlIndex in url:
                ydl.extract_info(urlIndex, download=True)
        else:
            ydl.download(url)



def download():
    if args.ignore == False:
        if helper.checkIfConfigEmpty():
            helper.WARNING("Config file is empty")
            helper.onelineInfo("Please add your credentials to the config file")
            return
        if helper.checkForConfigBlanks() == True:
            helper.ERROR("config.json is missing some values")
            return
    if json.loads(open("config.json").read())["written"] == True and helper.isDebug() == False:
        sender = json.loads(open("config.json").read())["username"]
        password = json.loads(open("config.json").read())["password"]
        receiver = json.loads(open("config.json").read())["receiver"]
    else:
        sender   = helper.getSender()
        password = helper.getPassword() 
        receiver = helper.getReceiver()
        
    allSongs = helper.getAllDownloads()
    if len(allSongs) == 0:
        helper.INFO("No songs to download")
        return
    else:
        for i, song in enumerate(allSongs):
            print(f"[{i+1}/{len(allSongs)}] {allSongs[i]}")
            try:
                mail.send(sender, password, receiver, f"downloads/{song}", f"{song}", f"{song}")
            except smtplib.SMTPRecipientsRefused as traceback:
                helper.ERROR(f"{receiver} is not a valid email address", traceback)
                exit()
            except smtplib.SMTPAuthenticationError as traceback:
                helper.ERROR("Invalid username or password",traceback)
                exit()
        if helper.isDebug() == False:
            helper.emptyURLfile()


install()
download()
