import csv

TITLE = 0
SHOW_ID = 1
MEDIA_TYPE = 2
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

media_list_by_title = {}

class Media:
    """ A class to represent a single entry in the dataset """
    def __init__(self, title, show_id, media_type, director, cast, country, date_added,
                 release_year, rating, duration, listed_in, description, streaming_service):
        self.title = title
        self.show_id = show_id
        self.media_type = media_type
        self.director = director
        self.cast = cast
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.rating = rating
        self.duration = duration
        self.listed_in = listed_in
        self.description = description
        self.streaming_service = streaming_service

def import_and_process_data():
    data = import_data_to_3d_list()



def import_data_to_3d_list(
    netflix_path="Data/netflix_titles.csv",
    amazon_path="Data/amazon_prime_titles.csv",
    disney_path="Data/disney_plus_titles.csv",
    hulu_path="Data/hulu_titles.csv"
):
    netflix_data = []
    amazon_prime_data = []
    disney_plus_data = []
    hulu_data = []

    with open(netflix_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row.append("Netflix")
            netflix_data.append(row)

    with open(amazon_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row.append("Amazon Prime")
            amazon_prime_data.append(row)

    with open(disney_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row.append("Disney+")
            disney_plus_data.append(row)

    with open(hulu_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            row.append("Hulu")
            hulu_data.append(row)
    data = [
        netflix_data,
        amazon_prime_data,
        disney_plus_data,
        hulu_data
    ]
    return data

def process_data(data):
    for streaming_service_data in data:
        for entry in streaming_service_data:
            # Create a Media object for each row
            media = Media(
                title=entry[TITLE],
                show_id=entry[SHOW_ID],
                media_type=entry[MEDIA_TYPE],
                director=_make_set(entry[DIRECTOR]),
                cast=_make_set(entry[CAST]),
                country=_make_set(entry[COUNTRY]),
                date_added=entry[DATE_ADDED],
                release_year=entry[RELEASE_YEAR],
                rating=entry[RATING],
                duration=entry[DURATION],
                listed_in=_make_set(entry[LISTED_IN]),
                description=entry[DESCRIPTION],
                streaming_service=entry[STREAMING_SERVICE]
            )
            add_media_by_title(media)


def _make_set(string):
    """ Helper function to convert a string to a set """
    return set(string.split(", "))

def add_media_by_title(media):
    global media_list_by_title
    """ Adds a movie or series to the media_by_title dictionary """
    if media.title not in media_list_by_title:
        media_list_by_title[media.title] = media
    else:
        # If the title already exists, add the streaming service to the existing entry
        media_list_by_title[media.title].streaming_service.add(media.streaming_service)
