from youtubesearchpython import VideosSearch
import argparse
parser = argparse.ArgumentParser(description='Search for a video on youtube')
parser.add_argument('--search', "-s", metavar='search', type=str, help='the search term')
parser.add_argument("--verbose", "-v", action="store_true", help="verbose output")
args = parser.parse_args()

def searchVideo(search, verbose=False):
    hits = {}
    videosSearch = VideosSearch(search, limit = 1)
    results = videosSearch.result()
    hits["Link"] = results["result"][0]["link"] 
    hits["Song Title"] = results["result"][0]["title"]
    hits["Channel"] = results["result"][0]["channel"]["name"].lower().replace(" - topic", "")
    if verbose:
        for k,v in hits.items():
            print(f"{k}: {v}")
        return hits["Link"]
    else:
        return hits["Link"]

if args.search:
    result = searchVideo(args.search, verbose=args.verbose)
else:
    result = searchVideo(input("Search: "), verbose=args.verbose)
    
with open("devTools/urls.txt", "a") as f:
    f.writelines(f"{result}\n")
