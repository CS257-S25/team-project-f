"""
cl.py

Command Line Interface for StreamSearch
This module provides a command line interface for the StreamSearch application.
It allows users to filter movies and shows based on actor names, categories, and release years.
"""
import argparse
from ProductionCode.datasource import DataSource

def parse_args():
    """
    Parses command line arguments for filtering movies/shows.
    """
    parser = argparse.ArgumentParser(
        prog="StreamSearch",
        description="Search for movies/shows across streaming platforms."
    )
    parser.add_argument('-a', '--actor', type=str, help='Filter by actor name')
    parser.add_argument('-c', '--category', type=str, help='Filter by category')
    parser.add_argument('-y', '--year', type=int, help='Filter by release year')
    return parser.parse_args()

def get_cl_filtered_results(args, ds):
    """
    Applies filtering logic based on command line arguments and calls the appropriate
    method from the DataSource.

    Parameters:
        args (Namespace): Parsed command line arguments containing actor, category, and/or year.
        ds (DataSource): An instance of the DataSource class to query media data from.

    Returns:
        list: A list of media entries (tuples) that match the given filters.
    """
    if args.actor and not args.category and not args.year:
        return ds.get_media_by_actor(args.actor)
    if args.category and not args.actor and not args.year:
        return ds.get_media_by_category(args.category)
    if args.year and not args.actor and not args.category:
        return ds.get_media_later_than(args.year)
    return ds.get_media_by_advanced_filter(
        args.actor if args.actor else '',
        args.year if args.year else 0,
        args.category if args.category else ''
    )

def display_results(results):
    """
    Displays query results in a readable format.

    Parameters:
        results (list of tuples): Each tuple represents a media record retrieved from the data source.
                                  Fields are printed separated by vertical bars.

    Output:
        Prints each result on a separate line. If no results are found, a corresponding message is displayed.
    """
    if not results:
        print("No matching results found.")
        return

    for row in results:
        print(" | ".join(str(field) for field in row))

def main():
    """
    Main function to parse command line arguments and fetch data from the DataSource.
    """
    args = parse_args()

    if not (args.actor or args.category or args.year):
        print("Please provide at least one filter: --actor, --category, or --year")
        return

    ds = DataSource()
    results = get_cl_filtered_results(args, ds)
    display_results(results)

if __name__ == "__main__":
    main()
