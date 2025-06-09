"""
test_cl.py
Unit tests for the command-line interface of the StreamSearch application.
"""

import unittest
import sys
from unittest.mock import patch
from io import StringIO
import cl

class MockDataSource:
    """
    mock of the DataSource class used to return predictable results
    based on specific test inputs.
    """

    def __init__(self):
        self.actor_results = [["Title A", "2022", "Action"]]
        self.category_results = [["Title B", "2021", "Drama"]]
        self.year_results = [["Title C", "2023", "Comedy"]]
        self.combo_results = [["Title D", "2024", "Action"]]
        self.empty_results = []

    def get_media_by_actor(self, actor):
        """
        Return mock results if the actor matches 'Actor X', otherwise empty list.
        """
        return self.actor_results if actor == "Actor X" else self.empty_results

    def get_media_by_category(self, category):
        """
        Return mock results if the category matches 'Drama', otherwise empty list.
        """
        return self.category_results if category == "Drama" else self.empty_results

    def get_media_later_than(self, year):
        """
        Return mock results if the year matches 2022, otherwise empty list.
        """
        return self.year_results if year == 2022 else self.empty_results

    def get_media_by_advanced_filter(self, actor, year, category):
        """
        Return mock results if all three filters match specific expected values,
        otherwise empty list.
        """
        if actor == "Actor X" and year == 2023 and category == "Action":
            return self.combo_results
        return self.empty_results


class TestCommandLineInterface(unittest.TestCase):
    """
    Unit tests for the StreamSearch command-line interface.
    """

    def setUp(self):
        """
        Set up a patched version of the DataSource.
        """
        self.patcher = patch("cl.DataSource", new=MockDataSource)
        self.patcher.start()

        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        """
        Restore stdout.
        """
        self.patcher.stop()
        sys.stdout = self.original_stdout

    def call_main_with_args(self, args):
        """
        Helper method to call the CLI's main() function with custom arguments.
        Returns the printed output as a string.
        """
        with patch.object(sys, "argv", ["cl.py"] + args):
            cl.main()
        return self.captured_output.getvalue().strip()

    def test_no_arguments(self):
        """
        Test that the CLI prints a prompt when no arguments are passed.
        """
        output = self.call_main_with_args([])
        self.assertIn("Please provide at least one filter", output)

    def test_filter_by_actor(self):
        """
        Test filtering by actor only.
        Should match results returned by get_movie_titles_by_actor().
        """
        output = self.call_main_with_args(["-a", "Actor X"])
        self.assertIn("Title A | 2022 | Action", output)

    def test_filter_by_category(self):
        """
        Test filtering by category only.
        Should match results returned by get_movies_by_category().
        """
        output = self.call_main_with_args(["-c", "Drama"])
        self.assertIn("Title B | 2021 | Drama", output)

    def test_filter_by_year(self):
        """
        Test filtering by year only.
        Should match results returned by get_movies_later_than().
        """
        output = self.call_main_with_args(["-y", "2022"])
        self.assertIn("Title C | 2023 | Comedy", output)

    def test_combined_filters(self):
        """
        Test filtering with all three arguments: actor, category, and year.
        Should match results returned by get_3_filter_media().
        """
        output = self.call_main_with_args(["-a", "Actor X", "-c", "Action", "-y", "2023"])
        self.assertIn("Title D | 2024 | Action", output)

    def test_no_results(self):
        """
        Test that the CLI properly handles when no results match the filter.
        """
        output = self.call_main_with_args(["-c", "Fantasy"])
        self.assertIn("No matching results found", output)
