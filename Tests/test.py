import unittest
import sys
from io import StringIO
from ProductionCode import data_import
from cl import add_all_titles, get_row_from_title, filter_movies_with_actor, filter_movies_by_genre, filter_movies_after_including_year, main

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

class TestCLFunctions(unittest.TestCase):

    def setUp(self):
        """ Load data for the tests, import data and initialize the titles set """
        netflix_path = "Dummy_data/dummy_netflix.csv"
        hulu_path = "Dummy_data/dummy_hulu.csv"
        amazon_path = "Dummy_data/dummy_amazon.csv"
        disney_path = "Dummy_data/dummy_disney.csv"

        self.netflix, self.amazon, self.disney, self.hulu = data_import.import_data(
            netflix_path=netflix_path,
            amazon_path=amazon_path,
            disney_path=disney_path,
            hulu_path=hulu_path
        )

        # Initialize a set for the titles
        self.titles = set()
        add_all_titles(
            self.titles,
            self.netflix,
            self.amazon,
            self.disney,
            self.hulu
        )

    def test_add_all_titles(self):
        """Verify that titles from each streaming platform are added to the set."""
        self.assertIn("Dick Johnson Is Dead", self.titles)  # From Netflix
        self.assertIn("Ricky Velez: Here's Everything", self.titles)  # From Hulu

    def test_filter_movies_with_actor(self):
        """Check if filtering by actor includes correct titles and excludes others."""
        filter_movies_with_actor("Brendan Gleeson", self.titles)  # From amazon
        self.assertIn("The Grand Seduction", self.titles)
        filter_movies_with_actor("Nonexistent Actor", self.titles)
        self.assertNotIn("The Grand Seduction", self.titles)  # Should be removed because the actor is not found

    def test_filter_movies_by_genre(self):
        """Test filtering by genre includes matching titles and excludes mismatches."""
        filter_movies_by_genre("Documentaries", self.titles)  # From Netflix
        self.assertIn("Dick Johnson Is Dead", self.titles)
        filter_movies_by_genre("Comedy", self.titles)
        self.assertNotIn("Dick Johnson Is Dead", self.titles)

    def test_filter_movies_after_including_year(self):
        """Verify that filtering by release year includes only movies from that year or later."""
        filter_movies_after_including_year(1988, self.titles)
        self.assertIn("Ernest Saves Christmas", self.titles)
        filter_movies_after_including_year(2021, self.titles)
        self.assertNotIn("Dick Johnson Is Dead", self.titles) 

    def test_get_row_from_title(self):
        """Ensure correct row is returned for a given movie title."""
        row = get_row_from_title("Dick Johnson Is Dead")
        self.assertEqual(row[TITLE], "Dick Johnson Is Dead")
        self.assertEqual(row[TYPE], "Movie")
        self.assertEqual(row[DIRECTOR], "Kirsten Johnson")

class TestMainCLIWithStringIO(unittest.TestCase):
    """Integration tests for the CLI main function using mocked command-line arguments."""

    def run_main_with_args(self, args_list):
        """
        Helper method to run the main CLI with specified arguments and capture its output.
        Returns output as a list of strings (each line).
        """
        original_stdout = sys.stdout
        original_argv = sys.argv
        sys.stdout = StringIO()
        sys.argv = ['cl.py'] + args_list

        try:
            main()
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = original_stdout
            sys.argv = original_argv

        return output.strip().split('\n')

    def test_actor_filter(self):
        """Test CLI output when filtering by actor."""
        output = self.run_main_with_args(['--actor', 'Brendan Gleeson'])
        self.assertIn("The Grand Seduction", output)

    def test_genre_filter(self):
        """Test CLI output when filtering by genre."""
        output = self.run_main_with_args(['--genre', 'Documentaries'])
        self.assertIn("Dick Johnson Is Dead", output)

    def test_year_filter_excludes_older_movies(self):
        """Test that filtering by year excludes movies released before the given year."""
        output = self.run_main_with_args(['--year', '2021'])
        self.assertNotIn("Dick Johnson Is Dead", output)

    def test_combined_filters(self):
        """Test combining actor and genre filters returns expected results."""
        output = self.run_main_with_args(['--actor', 'Brendan Gleeson', '--genre', 'Comedy'])
        self.assertIn("The Grand Seduction", output)


if __name__ == "__main__":
    unittest.main()