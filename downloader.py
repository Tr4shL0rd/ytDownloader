#!/usr/bin/env python3
import smtplib
#import youtube_dl
import yt_dlp as youtube_dl
import devTools.helper as helper
import devTools.mail as mail
import json
import devTools.downloaderArgs as downloaderArgs


args = downloaderArgs.parser.parse_args()
if args.ignore:
    helper.INFO("Ignoring errors")
if args.version:
    helper.getVersion()
    exit()


def install():
    #Gets the youtube-dl options from helper
    ydlOpts = helper.ydlOpts
    if args.quite:
        ydlOpts["quiet"] = True
        ydlOpts.pop("logger")
        ydlOpts.pop("progress_hooks")
    url = helper.urlReader()

    #Downloads the youtube url from the urls file 
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        i = 0
        for urlIndex in url:
            i += 1
            if args.no_download:
                ydl.extract_info(urlIndex, download=False)
            else:
                data = ydl.extract_info(urlIndex, download=False)
                print(f"[{i}/{len(url)}] {helper.fixSongNames(data['title'])}")
                ydl.download([urlIndex])



def download(quite=False):
    helper.fixDownloadedSongNames()
    if args.ignore == False:
        if helper.checkIfConfigEmpty():
            helper.WARNING("Config file is empty")
            helper.onelineInfo("Please add your credentials to the config file")
            return
        #checks if any of the config.json fields contain "___ BLANK!" 
        if helper.checkForConfigBlanks():
            helper.ERROR("config.json is missing some values")
            return
    # reads the config.json file and loads the fields into variables
    if json.loads(open("config.json").read())["written"] == True and helper.isDebug() == False:
        sender   = json.loads(open("config.json").read())["username"]
        password = json.loads(open("config.json").read())["password"]
        receiver = json.loads(open("config.json").read())["receiver"]
    else: #or reads the .env file 
        sender   = helper.getSender()
        password = helper.getPassword() 
        receiver = helper.getReceiver()

    #gets all files from downloads/
    allSongs = helper.getAllDownloads()
    if len(allSongs) == 0:
        if args.no_color == False:
            helper.ERROR("No songs to download")
        elif args.no_color:
            helper.ncERROR("No songs to download")
        elif args.ignoreTrue:
            return 
    else:
        for i, song in enumerate(allSongs):
            # debug song is one of the test songs 
            if song in helper.debugSongs:
                allSongs.remove(song)

            if quite == False:
                print(f"[{i+1}/{len(allSongs)}] {song}")
            try:
                mail.send(sender, password, receiver, f"downloads/{song}", f"{song}", f"{song}")
            except smtplib.SMTPRecipientsRefused as traceback:
                if args.ignore:
                    return
                helper.ERROR(f"{receiver} is not a valid email address", traceback)
                return
            except smtplib.SMTPAuthenticationError as traceback:
                if args.ignore:
                    return
                helper.ERROR("Invalid username or password",traceback)
                return

try:
    install()
    download()
    # helper.emptyUrlFile()
    # helper.emptyDownloads()
except KeyboardInterrupt:
    print("\nExiting...")