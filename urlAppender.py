from sys import argv

import youtube_dl
import devTools.urlArgs as urlArgs
import devTools.helper as helper

def main():
    args = urlArgs.parser.parse_args()
    if args.url != None:
        
        with open(helper.urlsPath, "a") as urlFile:
            urlFile.write(f"\n{args.url}")
            try:
                print(f"appended: {args.url}\n"
                    f"Title: {helper.getYoutubeTitle(args.url)}\n"
                    f"ID: {helper.getYoutubeId(args.url)}")
            except youtube_dl.utils.DownloadError:
                pass ## youtube-dl already prints the error message
    else:
        try:
            print("usage: urlAppender.py [-h] [--url URL]\n"
                f"urlAppender.py: error: unrecognized arguments: {argv[1]}")
        except IndexError:
            print("usage: urlAppender.py [-h] [--url URL]")

helper.removeEmptyLines()
main()