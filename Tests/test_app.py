import unittest
from app import app
from unittest.mock import patch

class BaseTestCase(unittest.TestCase):
    """Base test case to set up the Flask test client."""
    def setUp(self):
        self.client = app.test_client()

class TestHomepage(BaseTestCase):
    """Test for homepage route."""

    def test_homepage(self):
        """Test the homepage route."""
        response = self.client.get('/')
        self.assertIn("StreamSearch", response.data.decode())

class TestErrorHandling(BaseTestCase):
    """Test for error handling routes."""

    def test_404_error(self):
        """Test the 404 error handler."""
        response = self.client.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Error 404 - Incorrect format.", response.data.decode())

    def test_500_error(self):
        """Test the 500 error handler."""
        response = self.client.get('/cause_500')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Error 500 - A python bug has occurred.", response.data.decode())

class TestFilterFunctions(BaseTestCase):
    """Test filter functions with mocked data source."""

    @patch('app.db.get_movie_titles_by_actor')
    def test_actor_filter_valid_result(self, mock_get_movies):
        """Test actor filter with a known actor using mock."""
        # Mock return value
        mock_get_movies.return_value = [
            ("The Grand Seduction", "A comedy about a small town...")
        ]

        response = self.client.get('/actor/BRENDAN_GLEESON')
        self.assertIn("The Grand Seduction", response.data.decode())

    @patch('app.db.get_movie_titles_by_actor')
    def test_actor_filter_no_result(self, mock_get_movies):
        """Test actor filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/actor/UNKNOWN_ACTOR')
        self.assertIn("No results found for actor", response.data.decode())

    @patch('app.db.get_movies_later_than')
    def test_year_filter_valid_result(self, mock_get_movies):
        """Test year filter with mocked results."""
        mock_get_movies.return_value = [
            ("Some Movie", "A sci-fi film.", "Sci-Fi", 2020)
        ]

        response = self.client.get('/year/2019')
        self.assertIn("Some Movie", response.data.decode())

    @patch('app.db.get_movies_later_than')
    def test_year_filter_no_result(self, mock_get_movies):
        """Test year filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/year/2050')
        self.assertIn("No movies found released after 2050", response.data.decode())
     
if __name__ == '__main__':
    unittest.main()
