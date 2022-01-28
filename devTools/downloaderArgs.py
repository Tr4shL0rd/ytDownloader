import argparse
parser = argparse.ArgumentParser()


parser.add_argument(
    "--ignore", "-i",
    help="Ignore errors (can lead to unexpected results)",
    dest="ignore",
    action="store_true"
)
parser.add_argument(
    "--no-download", "-nd",
    help="Don't download the songs",
    dest="no_download",
    action="store_true"
)