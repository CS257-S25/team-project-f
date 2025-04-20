'''
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''

from ProductionCode import data_import

[netflix_data, amazon_prime_data, disney_plus_data, hulu_data] = data_import.import_data()

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


def add_all_titles(titles_set):
    for row in netflix_data:
        titles_set.add(row[TITLE])
    for row in amazon_prime_data:
        titles_set.add(row[TITLE])
    for row in disney_plus_data:
        titles_set.add(row[TITLE])
    for row in hulu_data:
        titles_set.add(row[TITLE])




def get_row_from_title(title):
    for row in netflix_data:
        if title == row[TITLE]:
            return row
    for row in amazon_prime_data:
        if title == row[TITLE]:
            return row
    for row in disney_plus_data:
        if title == row[TITLE]:
            return row
    for row in hulu_data:
        if title == row[TITLE]:
            return row
    return None

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

titles = set()
add_all_titles(titles)
filter_movies_with_actor("Adam Sandler", titles)
filter_movies_by_genre("Action", titles)
titles_list = sorted(titles)
print(titles_list)