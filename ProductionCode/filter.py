class Filter:

    """ Class to filter movies based on actor, genre, and year """
    def __init__(self, data):
        self.media_dict = data.get_media_dict()
        self.filtered_media_dict = self.media_dict.copy()

    def filter_by_actor(self, name):
        """ Filters the titles set to only include titles with the specified actor """
        for title in self.filtered_media_dict.copy():
            cast = self.filtered_media_dict[title].cast
            if name.lower() not in (actor.lower() for actor in cast):
                del self.filtered_media_dict[title]

    def filter_by_category(self, category):
        for title in self.filtered_media_dict.copy():
            categories = self.filtered_media_dict[title].listed_in
            if category.lower() not in (cat.lower() for cat in categories):
                del self.filtered_media_dict[title]

    def filter_by_year_onward(self, year):
        for title in self.filtered_media_dict.copy():
            release_year = self.filtered_media_dict[title].release_year
            if int(year) > int(release_year):
                del self.filtered_media_dict[title]

    def get_filtered_media_dict(self):
        return self.filtered_media_dict
    
    def print_filtered_titles(self):
        for media in self.filtered_media_dict.values():
            print(media.title)
        
    def print_filtered_all(self):
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