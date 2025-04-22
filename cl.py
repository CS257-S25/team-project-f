'''
cl.py

Command Line Interface for StreamSearch
This module provides a command line interface for the StreamSearch application.
It allows users to filter movies and shows based on actor names, categories, and release years.
'''
import argparse
from ProductionCode import data as d
from ProductionCode import filter as f

parser = argparse.ArgumentParser(
    prog="StreamSearch",
    description=
    "A command line interface for searching for movies and shows " \
    "across multiple streaming platforms."
)
parser.add_argument('-a', '--actor', type=str, help='Filter by actor name')
parser.add_argument('-c', '--category', type=str, help='Filter by category')
parser.add_argument('-y', '--year', type=int, help='Filter by release year')

def main():
    """ Main function to handle command line arguments and filter titles """

    dataset = d.Data()
    filterset = f.Filter(dataset)

    args = parser.parse_args()
    #print(args.actor, args.category, args.year)

    if args.actor:
        filterset.filter_by_actor(args.actor)
    if args.category:
        filterset.filter_by_category(args.category)
    if args.year:
        filterset.filter_by_year_onward(args.year)

    filterset.print_filtered_titles()

if __name__ == "__main__":
    main()
