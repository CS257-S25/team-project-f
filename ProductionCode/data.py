"""
data.py

The purpose of this module is to import and process datasets from various streaming services.
It creates a 3D list of media entries and a dictionary indexed by title for easy access.
"""

import csv
from collections import OrderedDict

# Constants for the indices of dataset columns to make indexing easier.
SHOW_ID = 0
MEDIA_TYPE = 1
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
STREAMING_SERVICE = 12

class Data:
    """A class to represent the dataset of movies and shows from various streaming services"""

    def __init__(self):
        """
        Initializes the Data class by importing datasets from various streaming services
        and creating a list and dictionary of media entries.
        """
        self.media_list = import_all_datasets_to_list()
        self.media_dict = create_media_dict_by_title(self.media_list)
        self.category_set = create_category_set(self.media_list)

    def get_media_list(self):
        """
        Returns the list containing data for all shows/movies from all streaming services.
        [<service>, <row>, <column>]
        """
        return self.media_list

    def get_media_dict(self):
        """
        Returns the dictionary containing data for all shows/movies from all streaming services.
        {<title>: <Media object>}
        """
        return self.media_dict
    
    def get_category_set(self):
        """
        Returns a set containing all of the categories named within the data.
        """
        return self.category_set

    def print_media_list(self):
        """
        Prints the entire media list, including the data from all 4 streaming services.
        """
        for service in self.media_list:
            print(f"STREAMING SERVICE: {service}\n")
            for entry in service:
                print(f"{entry}\n")


class Media:
    """
    A class to represent a single movie or show entry from the dataset
    and all of its associated information.
    """

    def __init__(self, entry):
        fill_empty_fields(entry)
        self.attributes = []
        self.attributes[TITLE] = entry[TITLE]
        self.attributes[SHOW_ID] = entry[SHOW_ID]
        self.attributes[MEDIA_TYPE] = entry[MEDIA_TYPE]
        self.attributes[DIRECTOR] = _make_set(entry[DIRECTOR])
        self.attributes[CAST] = _make_set(entry[CAST])
        self.attributes[COUNTRY] = _make_set(entry[COUNTRY])
        self.attributes[DATE_ADDED] = entry[DATE_ADDED]
        self.attributes[RELEASE_YEAR] = entry[RELEASE_YEAR]
        self.attributes[RATING] = entry[RATING]
        self.attributes[DURATION] = entry[DURATION]
        self.attributes[LISTED_IN] = _make_set(entry[LISTED_IN])
        self.attributes[DESCRIPTION] = entry[DESCRIPTION]
        self.attributes[STREAMING_SERVICE] = entry[STREAMING_SERVICE]


def import_all_datasets_to_list(
    netflix_dataset="Data/netflix_titles.csv",
    amazon_dataset="Data/amazon_prime_titles.csv",
    disney_dataset="Data/disney_plus_titles.csv",
    hulu_dataset="Data/hulu_titles.csv",
):
    """
    Imports datasets from various streaming services and returns a list containing the data of 
    all 4.
    """
    netflix_data = []
    amazon_prime_data = []
    disney_plus_data = []
    hulu_data = []

    import_dataset_to_list(netflix_dataset, netflix_data, "Netflix")
    import_dataset_to_list(amazon_dataset, amazon_prime_data, "Amazon Prime")
    import_dataset_to_list(disney_dataset, disney_plus_data, "Disney+")
    import_dataset_to_list(hulu_dataset, hulu_data, "Hulu")

    media_list = [netflix_data, amazon_prime_data, disney_plus_data, hulu_data]
    return media_list


def import_dataset_to_list(dataset, data, streaming_service_name):
    """
    Imports the each cell from a CSV file into a list of rows
    and appends the streaming service name to each row.
    """
    with open(dataset, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row.append(streaming_service_name)
            data.append(row)


def create_media_dict_by_title(data):
    """
    Creates a dictionary of media entries indexed by their titles.
    Each entry is a Media object containing all the information about the movie or show.
    """
    media_dict = {}
    for streaming_service in data:
        for entry in streaming_service:
            # Create a Media object for each row
            media = Media(entry)
            _add_media_to_dict_by_title(media, media_dict)
    media_dict = sort_dict_by_key(media_dict)
    return media_dict


def _add_media_to_dict_by_title(media, media_dict):
    """
    Adds a Media object to the dictionary indexed by its title.
    If the title already exists, it adds another streaming service to the existing entry.
    """
    title = media.title

    if title not in media_dict:
        media_dict[title] = media
    else:
        for service in media_dict[title].streaming_service:
            media_dict[title].streaming_service.add(service)

def create_category_set(data):
    """
    Creates a set containing all the unique catergories named within all 4 datasets.
    """
    categories = set()
    for streaming_service in data:
        for entry in streaming_service:
            listed_categories = _make_set(entry[LISTED_IN])
            for category in listed_categories:
                categories.add(category)
    return categories


def fill_empty_fields(entry):
    """
    Fills empty fields in the entry with "Unspecified" to avoid issues with missing data.
    """
    for i, field in enumerate(entry):
        if field == "":
            field = "Unspecified"


def _make_set(string):
    """
    Converts a comma-separated string into a set of values.
    """
    return set(string.split(", "))


def sort_dict_by_key(d):
    """
    Sorts a dictionary by its keys and returns an OrderedDict.
    """
    return OrderedDict(sorted(d.items()))


def main():
    """
    Main function to test the Data class and its methods.
    """
    # data = Data()
    # data.print_media_list()


if __name__ == "__main__":
    main()
