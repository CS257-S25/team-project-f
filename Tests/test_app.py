"""
test_app.py

This module contains unit tests for the flask app of the media 
filtering application.
"""
import unittest
from unittest.mock import patch
from app import app

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
        self.assertIn("404 - StreamSearch", response.data.decode())

    def test_500_error(self):
        """Test the 500 error handler."""
        response = self.client.get('/cause_500')
        self.assertIn("500 - StreamSearch", response.data.decode())

class TestFilterFunctions(BaseTestCase):
    """Test filter functions with mocked data source."""

    @patch('app.ds.get_media_by_actor')
    def test_actor_filter_valid_result(self, mock_get_movies):
        """Test actor filter with a known actor using mock."""
        mock_get_movies.return_value = mock_get_movies.return_value = [
            ("movie", "The Grand Seduction", "BRENDAN GLEESON", 2013,
              "Comedy", "A comedy set in Newfoundland.", "Netflix")
        ]
        response = self.client.get('/actor/BRENDAN_GLEESON')
        self.assertIn("The Grand Seduction", response.data.decode())

    @patch('app.ds.get_media_by_actor')
    def test_actor_filter_no_result(self, mock_get_movies):
        """Test actor filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/actor/UNKNOWN_ACTOR')
        self.assertIn("No results found for actor", response.data.decode())

    @patch('app.ds.get_media_by_actor')
    def test_actor_filter_lookup_error(self, mock_get_movies):
        """Test actor filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/actor/ERROR_ACTOR')
        self.assertIn("Could not find actor: ERROR_ACTOR", response.data.decode())

    @patch('app.ds.get_media_later_than')
    def test_year_filter_valid_result(self, mock_get_movies):
        """Test year filter with mocked results."""
        mock_get_movies.return_value = [
            ("movie", "Some Movie", "Another Actor", 2021, "Drama", "A futuristic drama.", "Prime")
        ]
        response = self.client.get('/year/2019')
        self.assertIn("Some Movie", response.data.decode())

    @patch('app.ds.get_media_later_than')
    def test_year_filter_no_result(self, mock_get_movies):
        """Test year filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/year/2050')
        self.assertIn("No movies found released after 2050", response.data.decode())

    @patch('app.ds.get_media_later_than')
    def test_year_filter_lookup_error(self, mock_get_movies):
        """Test year filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/year/2010')
        self.assertIn("Could not find titles after year: 2010", response.data.decode())


    @patch('app.ds.get_media_by_category')
    def test_category_filter_valid_result(self, mock_get_movies):
        """Test category filter with mocked results."""
        mock_get_movies.return_value = [
            ("movie", "Action Movie", "Some Actor", 2022, "Action",
              "An action-packed thriller.", "Hulu")
        ]
        response = self.client.get('/category/Action')
        self.assertIn("Action Movie", response.data.decode())

    @patch('app.ds.get_media_by_category')
    def test_category_filter_no_result(self, mock_get_movies):
        """Test category filter with no results."""
        mock_get_movies.return_value = []

        response = self.client.get('/category/UnknownCategory')
        self.assertIn("No movies found in category: UnknownCategory", response.data.decode())

    @patch('app.ds.get_media_by_category')
    def test_category_filter_lookup_error(self, mock_get_movies):
        """Test category filter route when a LookupError is raised."""
        mock_get_movies.side_effect = LookupError("DB error")
        response = self.client.get('/category/Drama')
        self.assertIn("Could not find movies in category: Drama", response.data.decode())

    @patch('ProductionCode.datasource.DataSource.get_all_categories')
    @patch('ProductionCode.datasource.DataSource.get_all_actors')
    @patch('ProductionCode.datasource.DataSource.get_all_media_titles')
    def test_filter_form(self, mock_titles, mock_get_actors, mock_get_categories):
        """
        Test the filter form is rendered correctly and that
        available movie categories and actors are retrieved and 
        displayed from the database.
        """
        mock_get_categories.return_value = ['Comedy', 'Action']
        mock_get_actors.return_value = ['Brad Pitt', 'Sandra Bullock']
        mock_titles.return_value = ['Movie A', 'Movie B']

        response = self.client.get('/filter')
        html = response.data.decode()
        self.assertIn("Comedy", html)
        self.assertIn("Action", html)
        self.assertIn("Brad Pitt", html)
        self.assertIn("Sandra Bullock", html)

    @patch('app.ds.get_media_by_advanced_filter')
    def test_filter_results_all_filters(self, mock_filter):
        """
        Test when all query parameters are provided,
        the correct database method is called and the results are displayed.
        """
        mock_filter.return_value = [("movie", "Movie Title A", "Actor",
                                      2020, "Drama", "Description", "Netflix")]
        response = self.client.get('/filter/results?actor=Actor&year=2021&category=Drama')
        self.assertIn("Movie Title A", response.data.decode())

    @patch('app.ds.get_media_by_advanced_filter')

    def test_filter_results_actor_category(self, mock_filter):
        """
        Test with only actor and category filters,
        the correct database method is called and the results are displayed.
        """
        mock_filter.return_value = [("movie", "Action Star", "Some Actor", 2022,
                                      "Action", "Explosive movie", "Hulu")]
        response = self.client.get('/filter/results?actor=Some+Actor&category=Action')
        self.assertIn("Action Star", response.data.decode())
        mock_filter.assert_called_with("Some Actor", "0", "Action")

    @patch('app.ds.get_media_by_advanced_filter')
    def test_filter_results_actor_year(self, mock_filter):
        """
        Test /filter/results with actor and year filters,
        the correct database method is called and the results are displayed.
        """
        mock_filter.return_value = [("movie", "Comeback", "Old Actor", 2019,
                                      "Drama", "A comeback role", "Netflix")]
        response = self.client.get('/filter/results?actor=Old+Actor&year=2020')
        self.assertIn("Comeback", response.data.decode())
        mock_filter.assert_called_with("Old Actor", "2019", "")

    @patch('app.ds.get_media_by_advanced_filter')
    def test_filter_results_category_year(self, mock_filter):
        """
        Test /filter/results with category and year filters,
        the correct database method is called and the results are displayed.
        """
        mock_filter.return_value = [("movie", "Future Flick", "Lead", 2030,
                                      "Sci-Fi", "Set in space", "Disney+")]
        response = self.client.get('/filter/results?category=Sci-Fi&year=2029')
        self.assertIn("Future Flick", response.data.decode())
        mock_filter.assert_called_with("", "2028", "Sci-Fi")

if __name__ == '__main__':
    unittest.main()
