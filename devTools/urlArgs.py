import argparse
parser = argparse.ArgumentParser()


parser.add_argument(
    "--url", "-u",
    help="The Url to be appended to 'urls.txt'",
    dest="url"
)