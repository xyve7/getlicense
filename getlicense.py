#!/usr/bin/python3

import requests as rq
import argparse as ap
import sys
import os
import datetime

# Parse command line arguments
parser = ap.ArgumentParser()
# Create the subparser 
subparser = parser.add_subparsers(title="Subcommands", dest="command")

# 'add' command parser
add_parser = subparser.add_parser("add", aliases=["a"], help="Adds a license")

# Arguments for the 'add' command
add_parser.add_argument("-l", "--license",  help="Key of the license", type=str)
add_parser.add_argument("-p", "--path", help="Path to write the license to", type=str, nargs="?")
add_parser.add_argument("-y", "--year", help="Year of the copyright", type=str, default=(str(datetime.date.today().year)), nargs="?")
add_parser.add_argument("-n", "--name", help="Name of the copyright holder", type=str, default="John Doe", nargs="?")

list_parser = subparser.add_parser("list", aliases=["l"], help="Lists available licenses")
args = parser.parse_args();

# Attempt to check for the token in the environment variable, if not found, abort
token = os.getenv("GITHUB_API_TOKEN")
if token is None:
    print("getlicense: Github token was note found! Set the 'GITHUB_API_TOKEN' environment variable as your token!", file=sys.stderr)
    sys.exit(1)

# Checks which subcommand was passed
match args.command:
    case "add" | "a":
        # Check if the argument parser found a license given by the user
        if args.license:
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
            }
            url = f"https://api.github.com/licenses/{args.license}"
            resp = rq.get(url, headers=headers)
            # Successful GET request
            if resp.status_code == 200:
                # If there is a file given, assign the output file to it, if not, write to stdout
                lfile = sys.stdout
                if args.path:
                    lfile = open(args.path, "w")

                # Write the license body data to the file, replacing the year and name correctly
                lfile.write(
                    resp.json()["body"]
                    .replace("[year]", args.year)
                    .replace("[fullname]", args.name)
                )
            else:
                print(
                    f"getlicense: unable to retrieve license {args.license}, status code: {resp.status_code}.",
                    file=sys.stderr,
                )
        # No license was provided, report error and exit
        else:
            print("getlicense: no license name given.", file=sys.stderr)

    case "list" | "l":
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
            }
            page = 1
            url = f"https://api.github.com/licenses"
            resp = rq.get(url, headers=headers, params={"page": page})
            # Successful GET request
            if resp.status_code == 200:
                while len(resp.json()) > 0:
                    for license in resp.json():
                        print(license["key"] + ": " + license["name"])
                    page += 1
                    url = f"https://api.github.com/licenses"
                    resp = rq.get(url, headers=headers, params={"page": page})
            else:
                print(
                    f"getlicense: unable to retrieve license list, status code: {resp.status_code}.",
                    file=sys.stderr,
                )
    case _:
        parser.print_help()

