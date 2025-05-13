"""
test_app.py

This module contains unit tests for the flask app of the media 
filtering application.
"""
import unittest
from unittest.mock import *
from ProductionCode import datasource
from app import app


class TestApp(unittest.TestCase):
    """Base test case to set up the Flask test client."""
    @patch('ProductionCode.datasource.psycopg2.connect')
    def setUp(self):
        self.client = app.test_client()
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    def test_homepage(self):
        """Test the homepage route."""
        response = self.client.get('/',follow_redirects=True)
        self.assertIn(b"Welcome to StreamSearch", response.data)

    def test_404_error(self):
        """Test the 404 error handler."""
        response = self.client.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Error 404 - Wrong Format", response.data)

    def test_500_error(self):
        """Test the 500 error handler."""
        response = self.client.get('/cause_500')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Error 500 - A python bug has occurred.", response.data)

    def test_actor_search(self, mock_connect):
        """Test actor search functionality."""
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = "The Croods"
        response = self.client.get('/actor/Emma%20Stone')
        self.assertIn(b"The Croods", response.data)

    def test_category_search(self,mock_connect):
        """Test actor search functionality."""
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = "Lieutenant Jangles"
        response = self.client.get('/category/Comedy')
        self.assertIn(b"Lieutenant Jangles", response.data)

    def test_year_search(self, mock_connect):
        """Test actor search functionality."""
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = "Cruising the Cut"
        response = self.client.get('/year/2010')
        self.assertIn(b"Cruising the Cut", response.data)

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

    @patch('app.db.get_movie_titles_by_actor')
    def test_actor_filter_lookup_error(self, mock_get_movies):
        """Test actor filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/actor/ERROR_ACTOR')
        self.assertIn("Could not find actor: ERROR_ACTOR", response.data.decode())

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

    @patch('app.db.get_movies_later_than')
    def test_year_filter_lookup_error(self, mock_get_movies):
        """Test year filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/year/2010')
        self.assertIn("Could not find titles after year: 2010", response.data.decode())


    @patch('app.db.get_movies_by_category')
    def test_category_filter_valid_result(self, mock_get_movies):
        """Test category filter with mocked results."""
        mock_get_movies.return_value = [
            ("Action Movie", "An action-packed adventure.", "Action", 2022)
        ]

        response = self.client.get('/category/Action')
        self.assertIn("Action Movie", response.data.decode())

    @patch('app.db.get_movies_by_category')
    def test_category_filter_no_result(self, mock_get_movies):
        """Test category filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/category/UnknownCategory')
        self.assertIn("No movies found in category: UnknownCategory", response.data.decode())

    @patch('app.db.get_movies_by_category')
    def test_category_filter_lookup_error(self, mock_get_movies):
        """Test category filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/category/Drama')
        self.assertIn("Could not find movies in category: Drama", response.data.decode())

if __name__ == '__main__':
    unittest.main()
