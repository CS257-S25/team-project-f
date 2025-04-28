"""
filtering.py

This module provides the Filter class for filtering media entries such as movies and TV shows.
Filters can be applied based on actor names, genres/categories, and release years. The class
operates on a dictionary of media objects and supports retrieving and printing the filtered results.
"""

from ProductionCode import formatting

class FilteredData:
    """
    Represents filted data (as created by the Filter class) as an object
    with various methods of accessing the data.
    """
    def __init__(self, filtered_data):
        """
        Initialize the filtered data object by having it store the filtered data
        dictionary.
        """
        self.data = filtered_data
    def get_data(self):
        """
        Return the filtered data dictionary.
        """
        return self.data()
    def get_titles_list(self):
        """
        Returns a list of the filtered media titles.
        """
        titles_list = []
        for title in self.data:
            titles_list.append(title)
        return titles_list
    def get_verbose_list(self):
        """
        Returns a list of the filtered media titles and all attributes.
        """
        verbose_list = []
        for media in self.data.values():
            verbose_list.append(media.str() + "\n\n")
    def get_web_displayable_titles(self):
        """
        Returns a string containing the titles of filtered media reformmated to be web
        displayable.
        """
        return formatting.make_list_web_displayable(self.get_titles_list())

class Filter:
    """
    Class with functions to easily filter movies based on actor, genre, and year.
    """
    def __init__(self, dataset):
        """
        Initializes the Filter with data from the dataset and creates a copy to be filtered.
        """
        self.dataset = dataset
        self.media_dict = self.dataset.get_media_dict()
        self.filtered_media_dict = self.media_dict.copy()

    def refresh(self):
        """
        Refreshes the filtered data when the filter needs to be used again.
        """
        self.filtered_media_dict = self.media_dict.copy()

    def filter_for_web(self, name, category, year):
        """
        Filters the dataset based on all the url parameters provided by a user 
        and returns a filtered data object.
        """
        self.refresh()
        filter_types = [self.filter_by_actor, self.filter_by_category,
                        self.filter_by_year_onward]
        user_inputs = [name, category, year]
        for filter_type, user_input in enumerate(user_inputs):
            if formatting.url_input_not_null(user_input):
                user_input = formatting.reformat_url_input(user_input)
                filter_types[filter_type](user_input)
        return FilteredData(self.filtered_media_dict)
    
    def filter_for_cl(self, name, category, year):
        """
        Filters the dataset based on all the arguments provided by a user 
        and returns the results as a filtered data object.
        """
        self.refresh()
        filter_types = [self.filter_by_actor, self.filter_by_category,
                        self.filter_by_year_onward]
        user_inputs = [name, category, year]
        for filter_type, user_input in enumerate(user_inputs):
            if user_input:
                filter_types[filter_type](user_input)
        return FilteredData(self.filtered_media_dict)

    def filter_by_actor(self, name):
        """
        Filters the media to only include entries featuring the specified actor.
        """
        for title in self.filtered_media_dict.copy():
            cast = self.filtered_media_dict[title].get_cast()
            if name.lower() not in (actor.lower() for actor in cast):
                del self.filtered_media_dict[title]

    def filter_by_category(self, category):
        """
        Filters the media to only include entries that belong to the specified genre/category.
        """
        for title in self.filtered_media_dict.copy():
            categories = self.filtered_media_dict[title].get_category()
            if category.lower() not in (cat.lower() for cat in categories):
                del self.filtered_media_dict[title]

    def filter_by_year_onward(self, year):
        """
        Filters the media to only include entries released in or after the specified year.
        """
        for title in self.filtered_media_dict.copy():
            release_year = self.filtered_media_dict[title].get_release_year()
            if int(year) > int(release_year):
                del self.filtered_media_dict[title]

    def filter_by_year_until(self, year):
        """
        Filters the media to only include entries released in or before the specified year.
        """
        for title in self.filtered_media_dict.copy():
            release_year = self.filtered_media_dict[title].get_release_year()
            if int(year) < int(release_year):
                del self.filtered_media_dict[title]
    
    def get_filtered_data(self):
        return FilteredData(self.filtered_media_dict)

        
