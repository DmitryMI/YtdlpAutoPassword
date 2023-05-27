import argparse
import subprocess
import re
from urllib.parse import urlparse

def get_password(csv_entries, domain, separator):
    for i, entry in enumerate(csv_entries):
        if not entry:
            continue
        items = entry.split(separator)
        url = items[0]
        login = items[1]
        pswrd = items[2]
        if domain in url:
            return login, pswrd
    return None, None

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("firefox_cmd")
    parser.add_argument("url")
    parser.add_argument("output_template")

    parser.add_argument("--csv_separator", required=False, default=";")
    args = parser.parse_args()

    cmd = args.firefox_cmd.split(" ")

    passwords_csv = subprocess.run(cmd, capture_output=True, text=True).stdout

    entries = passwords_csv.split("\n")[1:]

    url = args.url
    domain = urlparse(url).netloc
    if not domain:
        return 0

    login, pwd = get_password(entries, domain, args.csv_separator)
    if login:
        print(args.output_template % (login, pwd))
        return 0

    return 0

if __name__ == "__main__":
    code = main()
    quit(code)