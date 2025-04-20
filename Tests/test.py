import csv
import unittest
from ProductionCode import data_import  # noqa: E402
from cl import add_all_titles, get_row_from_title, filter_movies_with_actor, filter_movies_by_genre, filter_movies_after_including_year # noqa: E402

# Define global constants as they are in the main script
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

class TestCLI(unittest.TestCase):
    """
    Test cases for the command-line interface (CLI) functionality.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        This includes importing the data from dummydata.csv.
        """
        self.all_data = []
        with open("Data/dummydata.csv", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                self.all_data.append(row)

    def test_add_all_titles(self):
        """
        Test the add_all_titles function.
        Checks if all titles from all datasets are added to the set.
        """
        titles_set = set()
        add_all_titles(titles_set)
        expected_titles = {row[TITLE] for row in self.all_data}
        self.assertEqual(titles_set, expected_titles, "Test Failed: add_all_titles")

    def test_get_row_from_title(self):
        """
        Test the get_row_from_title function.
        Checks if the function returns the correct row for a given title.
        """
        # Test with a title that exists in the data
        if self.all_data:
            test_title = self.all_data[0][TITLE]
            expected_row = self.all_data[0]
            actual_row = get_row_from_title(test_title)
            self.assertEqual(actual_row, expected_row, "Test Failed: get_row_from_title - existing title")
        else:
            self.skipTest("No data available in dummydata.csv to perform this test.")

        # Test with a title that does not exist in the data
        test_title = "Nonexistent Title"
        expected_row = None
        actual_row = get_row_from_title(test_title)
        self.assertEqual(actual_row, expected_row, "Test Failed: get_row_from_title - nonexistent title")

    def test_filter_movies_with_actor(self):
        """
        Test the filter_movies_with_actor function.
        Checks if the function correctly filters movies based on actor name.
        """
        titles_set = {row[TITLE] for row in self.all_data}

        # Test with an actor that exists in some movies
        filter_movies_with_actor("Ama Qamata", titles_set)
        expected_titles = ("Blood & Water")
        self.assertEqual(titles_set, expected_titles, "Test Failed: filter_movies_with_actor - existing actor")
        # Test with an actor that does not exist in any movies
        filter_movies_with_actor("Nonexistent Actor", titles_set)
        expected_titles = set()
        self.assertEqual(titles_set, expected_titles, "Test Failed: filter_movies_with_actor - nonexistent actor")