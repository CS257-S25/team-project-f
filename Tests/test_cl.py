"""
test_cl.py

This module contains unit tests for the command line interface (CLI) of the media 
filtering application.
It tests the functionality of the command line arguments and their corresponding filters.
"""

import unittest
import sys
from unittest.mock import patch
from io import StringIO

from collections import OrderedDict

from ProductionCode import data as d
from ProductionCode.filtering import Filter
import cl

data = d.Data()

DATA1 = "Dummy_data/dummy_netflix.csv"
DATA2 = "Dummy_data/dummy_hulu.csv"
DATA3 = "Dummy_data/dummy_amazon.csv"
DATA4 = "Dummy_data/dummy_disney.csv"
data.media_list = d.import_all_datasets_to_list(
    netflix_dataset=DATA1,
    amazon_dataset=DATA2,
    disney_dataset=DATA3,
    hulu_dataset=DATA4,
)
data.media_dict = d.create_media_dict_by_title(data.media_list)
filtering = Filter(data)

class TestFilterFunctions(unittest.TestCase):
    """Test class for the Filter class and its methods."""

    def setUp(self):
        filtering.refresh()
        
    def test_filter_by_actor(self):
        """Check if filtering by actor includes only correct titles."""
        filtering.filter_by_actor("Brendan Gleeson")
        self.assertEqual(filtering.filtered_media_dict.keys(), {"The Grand Seduction"})

    def test_filter_by_nonexistent_actor(self):
        """Check if filtering by a nonexistent actor results in an empty dictionary."""
        filtering.filter_by_actor("Nonexistent Actor")
        self.assertEqual(filtering.filtered_media_dict.keys(), OrderedDict().keys())

    def test_filter_by_category(self):
        """Check if filtering by category includes only correct titles."""
        filtering.filter_by_category("Action")
        self.assertEqual(filtering.filtered_media_dict.keys(), OrderedDict().keys())

    def test_filter_by_category_lowercase(self):
        """Check if filtering by category in lowercase includes only correct titles."""
        filtering.filter_by_category("tv mysteries")
        self.assertEqual(filtering.filtered_media_dict.keys(), {"Blood & Water"})

    def test_filter_by_category_uppercase(self):
        """Check if filtering by category in uppercase includes only correct titles."""
        filtering.filter_by_category("DRAMA")
        self.assertEqual(
            filtering.filtered_media_dict.keys(),
            {
                "The Grand Seduction",
                "Take Care Good Night",
                "Silent Night",
            },
        )

    def test_filter_by_nonexistent_category(self):
        """Check if filtering by a nonexistent category results in an empty dictionary."""
        filtering.filter_by_category("spiders")
        self.assertEqual(filtering.filtered_media_dict.keys(), OrderedDict().keys())

    def test_filter_by_year_onward(self):
        """Check if filtering by a release year onwards includes only correct titles."""
        filtering.filter_by_year_onward(2021)
        self.assertEqual(
            filtering.filtered_media_dict.keys(),
            {"Blood & Water", "Ricky Velez: Here's Everything"},
        )

    def test_filter_by_year_until(self):
        """Check if filtering until a release year includes only correct titles."""
        filtering.filter_by_year_until(1999)
        self.assertEqual(
            filtering.filtered_media_dict.keys(),
            {"Ernest Saves Christmas"},
        )

    def test_print_filtered_titles(self):
        """Check if the printed titles after filtering are correct."""
        filtering.filter_by_actor("Brendan Gleeson")
        filtered_data = filtering.get_filtered_data()
        sys.stdout = StringIO()
        print(filtered_data.get_titles_list())
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output.strip(), "['The Grand Seduction']")


class TestCommandLineArguments(unittest.TestCase):
    """Test class for the command line interface of the media filtering application."""
    def setUp(self):
        self.mock_data = [
            [
                [
                    "s1",
                    "Movie",
                    "Title A",
                    "Director A",
                    "Actor X, Actor Y",
                    "USA",
                    "Jan 01, 2023",
                    "2022",
                    "PG",
                    "90 min",
                    "Action, Comedy",
                    "Description A",
                    "Service A",
                ]
            ],
            [
                [
                    "s2",
                    "Show",
                    "Title B",
                    "Director B",
                    "Actor Y, Actor Z",
                    "UK",
                    "Feb 15, 2023",
                    "2021",
                    "TV-MA",
                    "2 Seasons",
                    "Drama, Sci-Fi",
                    "Description B",
                    "Service B",
                ]
            ],
            [
                [
                    "s3",
                    "Movie",
                    "Title C",
                    "Director C",
                    "Actor X, Actor Z",
                    "Canada",
                    "Mar 20, 2023",
                    "2023",
                    "G",
                    "105 min",
                    "Comedy, Family",
                    "Description C",
                    "Service C",
                ]
            ],
            [
                [
                    "s4",
                    "Show",
                    "Title D",
                    "Director E",
                    "Actor W, Actor X",
                    "USA",
                    "May 05, 2024",
                    "2024",
                    "TV-Y",
                    "3 Seasons",
                    "Action, Drama",
                    "Description E",
                    "Service D",
                ]
            ],
            [
                [
                    "s5",
                    "Movie",
                    "Title G",
                    "",
                    "",
                    "",
                    "September 11, 2001",
                    "2020",
                    "",
                    "",
                    "Thriller",
                    "Description G",
                    "Service A",
                ]
            ],
        ]

        self.patcher = patch(
            "ProductionCode.data.import_all_datasets_to_list",
            return_value=self.mock_data,
        )
        self.mock_import = self.patcher.start()
        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output
        data.media_dict = d.create_media_dict_by_title(data.media_list)

    def tearDown(self):
        self.patcher.stop()
        sys.stdout = self.original_stdout

    def call_main_with_args(self, args):
        """Helper function to call the main function with command line arguments."""
        with patch("sys.argv", ["cl.py"] + args):
            cl.main()
        output = self.captured_output.getvalue()
        output = output.replace("'","")
        output = output.replace("[","")
        output = output.replace("]","")
        return output.strip().split(", ")

    def test_no_arguments(self):
        """Test the main function with no command line arguments."""
        output = self.call_main_with_args([])
        self.assertEqual(
            sorted(["Title A", "Title B", "Title C", "Title D", "Title G"]), sorted(output)
        )

    def test_filter_by_actor(self):
        """Test the main function with actor name as command line argument."""
        output = self.call_main_with_args(["-a", "Actor X"])
        self.assertEqual(sorted(["Title A", "Title C", "Title D"]), sorted(output))

    def test_filter_by_genre(self):
        """Test the main function with genre as command line argument."""
        output = self.call_main_with_args(["-c", "Comedy"])
        self.assertEqual(sorted(["Title A", "Title C"]), sorted(output))

    def test_filter_by_year(self):
        """Test the main function with year as command line argument."""
        output = self.call_main_with_args(["-y", "2022"])
        self.assertEqual(sorted(["Title A", "Title C", "Title D"]), sorted(output))

    def test_filter_by_actor_and_genre(self):
        """Test the main function with actor name and genre as command line arguments."""
        output = self.call_main_with_args(["-a", "Actor X", "-c", "Action"])
        self.assertEqual(sorted(["Title A", "Title D"]), sorted(output))


if __name__ == "__main__":
    unittest.main()
