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
parser.add_argument(
    "--version",
    help="Print the version",
    dest="version",
    action="store_true"
)
parser.add_argument(
    "--no-color", "-nc",
    help="Don't use colors",
    dest="no_color",
    action="store_true"
)
parser.add_argument(
    "--quite", "-q",
    help="Don't print anything",
    dest="quite",
    action="store_true"
)