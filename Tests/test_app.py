"""
test_cl.py

This module contains unit tests for the StreamSearch web application made for ID2.
It tests the functionality of the different routes and the filtering functions.
"""

import unittest
import app


class TestHomepage(unittest.TestCase):
    """Test the homepage route to ensure it contains the correct content."""

    def test_homepage(self):
        """Check if the homepage function returns the correct content."""
        expected_homepage = (
            "StreamSearch Individual Deliverable 2 - Johnathan Yu</br></br>"
            "To use this website, please insert the following into the address: "
            "/actor/category/year</br>"
            "actor: The name of an actor to search for in a movie/show's cast.</br>"
            "category: The category of movie/show to search for.</br>"
            "year: The results will only include moves released on or after this year.</br></br>"
            "IMPORTANT: All filters are optional. To omit a filter, replace it with "
            '"-", "_", or "x".</br>'
            "To represent spaces, either type the space normally, "
            'or use "-", "_", or "%20".</br></br>'
            "To view a list of categories available, insert /categories into the address."
        )
        self.assertEqual(app.homepage(), expected_homepage)


class TestCategoriesPage(unittest.TestCase):
    """Test the categories route to ensure it returns the correct categories."""

    def test_categories(self):
        """Check if the categories function returns the correct content."""
        expected_list = app.filters.dataset.get_category_set()
        expected_return = f"Valid categories are as follows:</br></br>{expected_list}"
        self.assertEqual(app.list_categories(), expected_return)


class TestFilterFunctions(unittest.TestCase):
    """Test class for the Filter class and its methods."""

    def test_all_filters_lowercase(self):
        """Check if filtering with all fields in lowercase includes only correct titles."""
        self.assertEqual(
            app.search_with_filters("brendan-gleeson", "comedy", "2010"),
            "The Grand Seduction</br>",
        )

    def test_all_filters_mixedcase(self):
        """Check if filtering with all fields in mixedcase includes only correct titles."""
        self.assertEqual(
            app.search_with_filters("bReNdan%20gleEsOn", "coMedy", "2010"),
            "The Grand Seduction</br>",
        )

    def test_all_filters_uppercase(self):
        """Check if filtering with all fields in uppercase includes only correct titles."""
        self.assertEqual(
            app.search_with_filters("BRENDAN_GLEESON", "COMEDY", "2010"),
            "The Grand Seduction</br>",
        )

    def test_actor_filter(self):
        """Check if filtering by actor includes only correct titles."""
        self.assertEqual(
            app.search_with_filters("john_lennon", "-", "-"),
            "The Beatles: Get Back</br>")

    def test_category_filter(self):
        """Check if filtering by category includes only correct titles."""
        results = (
            "A Muppets Christmas: Letters To Santa</br>"
            "Duck the Halls: A Mickey Mouse Christmas Special</br>"
            "Ice Age: A Mammoth Christmas</br>"
            "Secrets of the Zoo: Tampa</br>"
            "The Halloween Candy Magic Pet</br>"
        )
        self.assertEqual(app.search_with_filters("-", "family", "-"), results)

    def test_year_filter(self):
        """Check if filtering by year includes only correct titles."""
        results = (
            "Becoming Cousteau</br>"
            "Blood & Water</br>"
            "Gaia</br>"
            "Ganglands</br>"
            "Hawkeye</br>"
            "Jailbirds New Orleans</br>"
            "Kota Factory</br>"
            "Midnight Mass</br>"
            "My Little Pony: A New Generation</br>"
            "Queens</br>"
            "Ricky Velez: Here's Everything</br>"
            "Settlers</br>"
            "The Beatles: Get Back</br>"
            "The Great British Baking Show</br>"
            "The Halloween Candy Magic Pet</br>"
            "The Marksman</br>"
            "The Next Thing You Eat</br>"
            "The Queen Family Singalong</br>"
            "The Starling</br>"
        )
        self.assertEqual(app.search_with_filters("-", "-", "2021"), results)

    def test_two_filters(self):
        """Check if filtering by actor and category includes only correct titles."""
        results = "The Grand Seduction</br>"
        self.assertEqual(
            app.search_with_filters("brendan-gleeson", "comedy", "-"), results
        )

    def test_nonexistent_actor(self):
        """Check if filtering by a nonexistent actor results in an empty string."""
        self.assertEqual(app.search_with_filters("John-Yu", "-", "-"), "")


class TestErrorHandling(unittest.TestCase):
    """Test error handling for the application."""

    def test_404_error(self):
        """Check if the 404 error handler returns the correct content."""
        expected_error = (
            "Error 404 - Incorrect format.</br></br>"
            "To use this website, please insert the following into the address: "
            "/actor/category/year</br>"
            "actor: The name of an actor to search for in a movie/show's cast.</br>"
            "category: The category of movie/show to search for.</br>"
            "year: The results will only include moves released on or after this year.</br></br>"
            "IMPORTANT: All filters are optional. To omit a filter, replace it with "
            '"-", "_", or "x".</br>'
            "To represent spaces, either type the space normally, "
            'or use "-", "_", or "%20".</br></br>'
            "To view a list of categories available, insert /categories into the address."
        )
        self.assertEqual(app.page_not_found(None), expected_error)

    def test_500_error(self):
        """Check if the 500 error handler returns the correct content."""
        expected_error = "Error 500 - A python bug has occurred.</br></br>" \
            "Please check your input and try again."  
        self.assertEqual(app.python_bug(None), expected_error)


if __name__ == "__main__":
    unittest.main()
