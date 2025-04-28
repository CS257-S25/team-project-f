'''
cl.py

Command Line Interface for StreamSearch
This module provides a command line interface for the StreamSearch application.
It allows users to filter movies and shows based on actor names, categories, and release years.
'''
import argparse
from ProductionCode import filtering as f
from ProductionCode.data import Data

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
    dataset = Data()
    filtering = f.Filter(dataset)
    args = parser.parse_args()
    filtered_data = filtering.filter_for_cl(args.actor, args.category, args.year)
    print(filtered_data.get_titles_list())

if __name__ == "__main__":
    main()