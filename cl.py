"""
cl.py

Command Line Interface for StreamSearch
This module provides a command line interface for the StreamSearch application.
It allows users to filter movies and shows based on actor names, categories, and release years.
"""
import argparse
from ProductionCode.datasource import DataSource

parser = argparse.ArgumentParser(
    prog="StreamSearch",
    description="Search for movies/shows across streaming platforms."
)
parser.add_argument('-a', '--actor', type=str, help='Filter by actor name')
parser.add_argument('-c', '--category', type=str, help='Filter by category')
parser.add_argument('-y', '--year', type=int, help='Filter by release year')

def main():
    """
    Main function to parse command line arguments and fetch data from the DataSource.
    """
    args = parser.parse_args()
    ds = DataSource()

    if not (args.actor or args.category or args.year):
        print("Please provide at least one filter: --actor, --category, or --year")
        return

    results = ds.get_3_filter_media(
        args.actor if args.actor else '',
        args.year if args.year else '0',
        args.category if args.category else ''
    )

    if not results:
        print("No matching results found.")
    else:
        for row in results:
            print(" | ".join(str(field) for field in row))

if __name__ == "__main__":
    main()
