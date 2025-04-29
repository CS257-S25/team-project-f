import unittest
from app import app  # Import the Flask app

class TestHomepage(unittest.TestCase):
    
    def setUp(self):
        """Create a test client for the Flask app."""
        self.client = app.test_client()

    def test_homepage(self):
        """Test the homepage route."""
        response = self.client.get('/')
        expected_homepage = "StreamSearch</br></br>To use this website, please insert the following into the address: /actor/category/year</br>" \
                            "actor: The name of an actor to search for in a movie/show's cast.</br>" \
                            "category: The category of movie/show to search for.</br>" \
                            "year: The results will only include moves released on or after this year.</br></br>" \
                            "IMPORTANT: All filters are optional. To omit a filter, replace it with " \
                            "\"-\", \"_\", or \"x\".</br>" \
                            "To represent spaces, either type the space normally, " \
                            "or use \"-\", \"_\", or \"%20\".</br></br>" \
                            "To view a list of categories available, insert /categories into the address."
        self.assertEqual(response.data.decode(), expected_homepage)

class TestCategoryFilter(unittest.TestCase):

    def setUp(self):
        """Create a test client for the Flask app."""
        self.client = app.test_client()

    def test_list_categories(self):
        """Test that the categories route returns the correct categories list."""
        response = self.client.get('/categories')
        expected_categories = "TV Dramas"
        self.assertIn(expected_categories, response.data.decode())

class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        """Create a test client for the Flask app."""
        self.client = app.test_client()

    def test_404_error(self):
        """Test the 404 error handler."""
        response = self.client.get('/nonexistent_route')
        expected_error = "Error 404 - Incorrect format."
        self.assertIn(expected_error, response.data.decode())

class TestFilterFunctions(unittest.TestCase):

    def setUp(self):
        """Create a test client for the Flask app."""
        self.client = app.test_client()

    def test_actor_filter(self):
        """Test actor filter."""
        response = self.client.get('/BRENDAN_GLEESON/comedy/2010')
        expected_titles = "The Grand Seduction"
        self.assertIn(expected_titles, response.data.decode())

    def test_category_filter(self):
        """Test category filter."""
        response = self.client.get('/-/drama/2010')
        expected_titles = "A Promise to Astrid"
        self.assertIn(expected_titles, response.data.decode())

if __name__ == '__main__':
    unittest.main()
