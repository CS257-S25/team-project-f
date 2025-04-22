class Filter:

    """ Class to filter movies based on actor, genre, and year """
    def __init__(self, data):
        """
        Initializes the Filter object with media data.

        Args:
        
        data (MediaData): An object that provides the media data via get_media_dict().
        """
        self.media_dict = data.get_media_dict()
        self.filtered_media_dict = self.media_dict.copy()

    def filter_by_actor(self, name):
        """
        Filters media entries to include only those featuring the specified actor.

        Args:
            name (str): The name of the actor to filter by.
        """
        for title in self.filtered_media_dict.copy():
            cast = self.filtered_media_dict[title].cast
            if name.lower() not in (actor.lower() for actor in cast):
                del self.filtered_media_dict[title]

    def filter_by_category(self, category):
        """
        Filters media entries to include only those in the specified category or genre.

        Args:
            category (str): The category or genre to filter by.
        """
        for title in self.filtered_media_dict.copy():
            categories = self.filtered_media_dict[title].listed_in
            if category.lower() not in (cat.lower() for cat in categories):
                del self.filtered_media_dict[title]

    def filter_by_year_onward(self, year):
        """
        Filters media entries to include only those released in or after the specified year.

        Args:
            year (int or str): The minimum release year (inclusive).
        """
        for title in self.filtered_media_dict.copy():
            release_year = self.filtered_media_dict[title].release_year
            if int(year) > int(release_year):
                del self.filtered_media_dict[title]

    def get_filtered_media_dict(self):
        """
        Returns the filtered dictionary of media entries.

        Returns:
            dict: The filtered media dictionary.
        """
        return self.filtered_media_dict
    
    def print_filtered_titles(self):
        """
        Prints the titles of all filtered media entries.
        """
        for media in self.filtered_media_dict.values():
            print(media.title)
        
    def print_filtered_all(self):
        """
        Prints detailed information of all filtered media entries.
        """
        for media in self.filtered_media_dict.values():
            print(f"Title: {media.title}")
            print(f"Show ID: {media.show_id}")
            print(f"Media Type: {media.media_type}")
            print(f"Director: {media.director}")
            print(f"Cast: {media.cast}")
            print(f"Country: {media.country}")
            print(f"Date Added: {media.date_added}")
            print(f"Release Year: {media.release_year}")
            print(f"Rating: {media.rating}")
            print(f"Duration: {media.duration}")
            print(f"Listed In: {media.listed_in}")
            print(f"Description: {media.description}")
            print(f"Streaming Services: {media.streaming_service}\n")