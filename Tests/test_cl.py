import unittest
import sys
from unittest.mock import patch
from io import StringIO
from ProductionCode import data_setup
import cl

# Define global constants as they are in the main script
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

class TestFunctions(unittest.TestCase):
    def setUp(self):
        """Load data and initialize the titles set based on the new structure."""
        netflix_path = "Dummy_data/dummy_netflix.csv"
        hulu_path = "Dummy_data/dummy_hulu.csv"
        amazon_path = "Dummy_data/dummy_amazon.csv"
        disney_path = "Dummy_data/dummy_disney.csv"

        data = data_setup.import_data_to_3d_list(
            netflix_path=netflix_path,
            amazon_path=amazon_path,
            disney_path=disney_path,
            hulu_path=hulu_path
        )
        data_setup.process_data(data)
        self.media_list_by_title = data_setup.media_list_by_title
        self.titles = set(self.media_list_by_title.keys())

    def test_add_all_titles(self):
        """Verify that the correct titles are added."""
        expected_titles = {
            "The Grand Seduction",
            "Take Care Good Night",
            "Duck the Halls: A Mickey Mouse Christmas Special",
            "Ernest Saves Christmas",
            "Ricky Velez: Here's Everything",
            "Silent Night",
            "Dick Johnson Is Dead",
            "Blood & Water"
        }
        self.assertEqual(self.titles, expected_titles)

    def test_filter_movies_with_actor(self):
        """Check if filtering by actor includes only correct titles."""
        titles_copy = self.titles.copy()
        cl.filter_movies_with_actor("Brendan Gleeson", titles_copy, self.media_list_by_title)
        self.assertEqual(titles_copy, {"The Grand Seduction"})

        titles_copy = self.titles.copy()
        cl.filter_movies_with_actor("Nonexistent Actor", titles_copy, self.media_list_by_title)
        self.assertEqual(titles_copy, set())

    def test_filter_movies_by_genre(self):
        """Test filtering by genre."""
        titles_copy = self.titles.copy()
        cl.filter_movies_by_genre("Documentaries", titles_copy, self.media_list_by_title)
        self.assertEqual(titles_copy, {"Dick Johnson Is Dead"})

        titles_copy = self.titles.copy()
        cl.filter_movies_by_genre("Horror", titles_copy, self.media_list_by_title)
        self.assertEqual(titles_copy, set())

        titles_copy = self.titles.copy()
        cl.filter_movies_by_genre("Comedy", titles_copy, self.media_list_by_title)
        self.assertNotIn("Dick Johnson Is Dead", titles_copy)

    def test_filter_movies_after_including_year(self):
        """Verify filtering by release year."""
        titles_copy = self.titles.copy()
        cl.filter_movies_after_including_year(1988, titles_copy, self.media_list_by_title)
        self.assertIn("Ernest Saves Christmas", titles_copy)

        titles_copy = self.titles.copy()
        cl.filter_movies_after_including_year(2021, titles_copy, self.media_list_by_title)
        self.assertNotIn("Dick Johnson Is Dead", titles_copy)
        self.assertEqual(titles_copy, {
            "Ricky Velez: Here's Everything",
            "Blood & Water"
        })

    def test_get_row_from_title(self):
        """Ensure correct Media object is returned."""
        media = cl.get_row_from_title("Dick Johnson Is Dead", self.media_list_by_title)
        self.assertEqual(media.title, "Dick Johnson Is Dead")
        self.assertEqual(media.media_type, "Movie")
        self.assertEqual(media.director, {"Kirsten Johnson"})

class TestCommandLineArguments(unittest.TestCase):

    def setUp(self):
        self.mock_data = [
            [['s1', 'Movie', 'Title A', 'Director A', 'Actor X, Actor Y', 'USA', 'Jan 01, 2023', '2022', 'PG', '90 min', 'Action, Comedy', 'Description A']],
            [['s2', 'Show', 'Title B', 'Director B', 'Actor Y, Actor Z', 'UK', 'Feb 15, 2023', '2021', 'TV-MA', '2 Seasons', 'Drama, Sci-Fi', 'Description B']],
            [['s3', 'Movie', 'Title C', 'Director C', 'Actor X, Actor Z', 'Canada', 'Mar 20, 2023', '2023', 'G', '105 min', 'Comedy, Family', 'Description C']],
            [['s4', 'Show', 'Title D', 'Director E', 'Actor W, Actor X', 'USA', 'May 05, 2024', '2024', 'TV-Y', '3 Seasons', 'Action, Drama', 'Description E']]
        ]
        self.patcher = patch('ProductionCode.data_import.import_data', return_value=self.mock_data)
        self.mock_import = self.patcher.start()
        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        self.patcher.stop()
        sys.stdout = self.original_stdout

    def call_main_with_args(self, args):
        with patch('sys.argv', ['cl.py'] + args):
            cl.main()
        return self.captured_output.getvalue().strip().split('\n')

    def test_no_arguments(self):
        output = self.call_main_with_args([])
        self.assertEqual(sorted(['Title A', 'Title B', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_actor(self):
        output = self.call_main_with_args(['-a', 'Actor X'])
        self.assertEqual(sorted(['Title A', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_genre(self):
        output = self.call_main_with_args(['-g', 'Comedy'])
        self.assertEqual(sorted(['Title A', 'Title C']), sorted(output))

    def test_filter_by_year(self):
        output = self.call_main_with_args(['-y', '2022'])
        self.assertEqual(sorted(['Title A', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_actor_and_genre(self):
        output = self.call_main_with_args(['-a', 'Actor X', '-g', 'Action'])
        self.assertEqual(sorted(['Title A', 'Title D']), sorted(output))

if __name__ == '__main__':
    unittest.main()
