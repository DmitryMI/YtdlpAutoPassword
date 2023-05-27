import argparse
import subprocess
import re

def get_password(csv_entries, url_regex, separator):
    for i, entry in enumerate(csv_entries):
        items = entry.split(separator)
        url = items[0]
        login = items[1]
        pswrd = items[2]
        if re.match(url_regex, url):
            return login, pswrd
    return None, None

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("firefox_cmd")
    parser.add_argument("url_regex")
    parser.add_argument("output_template")

    parser.add_argument("--csv_separator", required=False, default=";")
    args = parser.parse_args()

    cmd = args.firefox_cmd.split(" ")

    passwords_csv = subprocess.run(cmd, capture_output=True, text=True).stdout

    entries = passwords_csv.split("\n")[1:]

    login, pwd = get_password(entries, args.url_regex, args.csv_separator)
    if login:
        print(args.output_template % (login, pwd))
        return 0

    return 1

if __name__ == "__main__":
    code = main()
    quit(code)