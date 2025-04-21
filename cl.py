'''
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''
import argparse 
from ProductionCode import data_import

SHOW_ID = 0
TYPE = 1
TITLE = 2
DIRECTOR = 3
CAST = 4
COUNTRY = 5
DATE_ADDED = 6
RELEASE_YEAR = 7
RATING = 8
DURATION = 9
LISTED_IN = 10
DESCRIPTION = 11

parser = argparse.ArgumentParser(
    prog="StreamSearch",
    description="A command line interface for searching for movies and shows across multiple streaming platforms."
)
parser.add_argument('-a', '--actor', type=str, help='Filter by actor name')
parser.add_argument('-g', '--genre', type=str, help='Filter by genre')
parser.add_argument('-y', '--year', type=int, help='Filter by release year')

title_dict = {}

def add_all_titles(titles_set, netflix_data, amazon_prime_data, disney_plus_data, hulu_data):
    global title_dict
    for row in netflix_data:
        title_dict[row[TITLE]] = row
        titles_set.add(row[TITLE])
    for row in amazon_prime_data:
        title_dict[row[TITLE]] = row
        titles_set.add(row[TITLE])
    for row in disney_plus_data:
        title_dict[row[TITLE]] = row
        titles_set.add(row[TITLE])
    for row in hulu_data:
        title_dict[row[TITLE]] = row
        titles_set.add(row[TITLE])

def get_row_from_title(title):
    return title_dict[title]

def filter_movies_with_actor(actor_name, titles_set):
    actor_name = actor_name.lower()
    titles_set_copy = titles_set.copy()
    for title in titles_set_copy:
        row = get_row_from_title(title)
        if actor_name not in row[CAST].lower():
            titles_set.remove(title)

def filter_movies_by_genre(genre_name, titles_set):
    genre_name = genre_name.lower()
    titles_set_copy = titles_set.copy()
    for title in titles_set_copy:
        row = get_row_from_title(title)
        if genre_name not in row[LISTED_IN].lower():
            titles_set.remove(title)

def filter_movies_after_including_year(year, titles_set):
    year = int(year)
    titles_set_copy = titles_set.copy()
    for title in titles_set_copy:
        row = get_row_from_title(title)
        if int(row[RELEASE_YEAR]) < year:
            titles_set.remove(title)

def main():
    [netflix_data, amazon_prime_data, disney_plus_data, hulu_data] = data_import.import_data()
    args = parser.parse_args()
    print(args.actor, args.genre, args.year)

    titles = set()
    add_all_titles(titles, netflix_data, amazon_prime_data, disney_plus_data, hulu_data)

    if args.actor:
        filter_movies_with_actor(args.actor, titles)
    if args.genre:
        filter_movies_by_genre(args.genre, titles)
    if args.year:
        filter_movies_after_including_year(args.year, titles)

    titles_list = sorted(titles)
    for title in titles_list:
        print(title)

if __name__ == "__main__":
    main()
