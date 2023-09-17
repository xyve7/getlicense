#!/usr/bin/python3

import requests as rq
import argparse as ap
import sys
import os
import datetime

# Parser the command-line arguments
arg_parser = ap.ArgumentParser()
arg_parser.add_argument("license", help="Name of the license", type=str)
arg_parser.add_argument(
    "path", help="Path to the file to write the license to", type=str, nargs="?"
)
arg_parser.add_argument(
    "year",
    help="Year for the copyright of the license",
    type=str,
    default=str(datetime.date.today().year),
    nargs="?",
)

arg_parser.add_argument(
    "name",
    help="Name for the copyright holder",
    type=str,
    default="John Doe",
    nargs="?",
)
args = arg_parser.parse_args()

# Attempt to check for the token in the environment variable, if not found, abort
token = os.getenv("GITHUB_API_TOKEN")
if token is None:
    print(
        "getlicense: github token was not found. get the 'GITHUB_API_TOKEN' environment variable to the token.",
        file=sys.stderr,
    )
    sys.exit(1)

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
