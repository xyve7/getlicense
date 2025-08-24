#!/usr/bin/python3

import requests as rq
import argparse as ap
import sys
from rapidfuzz import fuzz

# Parse command line arguments
parser = ap.ArgumentParser()
# Create the subparser 
subparser = parser.add_subparsers(title="Subcommands", dest="command")
# 'search' command parser
search_parser = subparser.add_parser("search", aliases=["s"], help="Search for a license")
search_parser.add_argument("query");
search_parser.add_argument("-c", "--count", help="Number of entries to display", type=int, default=10, nargs="?");
# 'add' command parser
get_parser = subparser.add_parser("get", aliases=["g"], help="Gets a license")
# Arguments for the 'add' command
get_parser.add_argument("license", help="Key of the license", type=str)
# 'list' command parser
list_parser = subparser.add_parser("list", aliases=["l"], help="Lists available licenses")
args = parser.parse_args();

# Error function
def fatal(message: str) -> None:
    print(f"[getlicense] FATAL: {message}", file=sys.stderr)
    sys.exit(1)

def main() -> None:
    # Checks which subcommand was passed
    match args.command:
        case "search" | "s":
            if not args.query:
                fatal("No search query given")
            
            response = rq.get("https://spdx.org/licenses/licenses.json")
            if response.status_code != 200:
                fatal(f"Unable to retrieve license list, code: {response.status_code}")
            
            json = response.json()
            licenses = json['licenses']
            print("{: <40} {}".format("License ID", "License Name"))

            results = []
            for license in licenses:
                name = license['name']
                id = license['licenseId']
                probability = max(fuzz.ratio(name, args.query), fuzz.ratio(id, args.query))
                results.append((probability, license))
            
            results.sort(key=lambda x: x[0])
            results.reverse()

            for result in results[:args.count]:
                print("{: <40} {}".format(result[1]['licenseId'], result[1]['name']))
        
        case "get" | "g":
            if not args.license:
                fatal("No license ID provided")

            response = rq.get(f"https://spdx.org/licenses/{args.license}.json")
            if response.status_code == 404:
                fatal(f"{args.license} is NOT a valid license ID!")
            
            if response.status_code != 200:
                fatal(f"Unable to retrieve license {args.license}, code: {response.status_code}")

            json = response.json()
            sys.stdout.write(json['licenseText'])
        
        case "list" | "l":
            response = rq.get("https://spdx.org/licenses/licenses.json")
            if response.status_code != 200:
                fatal(f"Unable to retrieve license list! Code: {response.status_code}")
            
            json = response.json()
            licenses = json['licenses']
            print("{: <40} {}".format("License ID", "License Name"))

            for license in licenses:
                id = license['licenseId']
                name = license['name']
                print("{: <40} {}".format(id, name))
        
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()

