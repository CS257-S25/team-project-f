"""
Unit tests for the DataSource class in datasource.py.
Uses mock objects to simulate database interactions.
"""
import unittest
from unittest.mock import patch, MagicMock
import psycopg2
from ProductionCode.datasource import DataSource

class TestDataSource(unittest.TestCase):
    """
    Unit tests for the DataSource class in datasource.py.
    Uses mock objects to simulate database interactions.
    """

    def setUp(self):
        """
        Sets up a mock database connection and cursor.
        """
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    def get_connected_datasource(self, mock_connect):
        """
        Helper function to return a connected DataSource using mock connection.
        """
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        ds.connect()
        return ds

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """
        Test successful database connection.
        """
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        conn = ds.connect()

        self.assertEqual(conn, self.mock_conn)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_later_than(self, mock_connect):
        """
        Test get_movies_later_than returns expected movie data.
        """
        self.mock_cursor.fetchall.return_value = [('Movie A', 2022)]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_movies_later_than(2020)

        self.assertEqual(result, [('Movie A', 2022)])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movie_titles_by_actor(self, mock_connect):
        """
        Test get_movie_titles_by_actor returns movies matching actor name.
        """
        self.mock_cursor.fetchall.return_value = [('Movie X', 'Actor Y')]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_movie_titles_by_actor("Actor Y")

        self.assertEqual(result, [('Movie X', 'Actor Y')])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_by_category(self, mock_connect):
        """
        Test get_movies_by_category returns movies matching category.
        """
        self.mock_cursor.fetchall.return_value = [('Movie B', '2021')]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_movies_by_category("Horror")

        self.assertEqual(result, [('Movie B', '2021')])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_categories(self, mock_connect):
        """
        Test get_all_categories returns unique categories split from comma-separated values.
        """
        self.mock_cursor.fetchall.return_value = [("Action, Drama",), ("Comedy",),
                                                   ("Drama, Sci-Fi",)]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_all_categories()

        self.assertEqual(result, ['Action', 'Comedy', 'Drama', 'Sci-Fi'])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_3_filter_media(self, mock_connect):
        """
        Test get_3_filter_media returns media filtered by actor, year, and category.
        """
        self.mock_cursor.fetchall.return_value = [('Movie Z', 2023)]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_3_filter_media("Actor A", "2020", "Thriller")

        self.assertEqual(result, [('Movie Z', 2023)])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_connect_database_error(self, mock_connect):
        """
        Test that connect() raises a ConnectionError when database connection fails.
        """
        mock_connect.side_effect = psycopg2.DatabaseError("DB connection failed")

        ds = DataSource()
        with self.assertRaises(ConnectionError) as context:
            ds.connect()

        self.assertIn("Connection error", str(context.exception))

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_later_than_query_error(self, mock_connect):
        """
        Test get_movies_later_than returns None on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

        ds = DataSource()
        ds.connect()
        result = ds.get_movies_later_than(2020)

        self.assertIsNone(result)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movie_titles_by_actor_query_error(self, mock_connect):
        """
        Test get_movie_titles_by_actor returns None on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

        ds = DataSource()
        ds.connect()
        result = ds.get_movie_titles_by_actor("Actor Y")

        self.assertIsNone(result)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movie_by_category_query_error(self, mock_connect):
        """
        Test get_movies_by_category returns None on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

        ds = DataSource()
        ds.connect()
        result = ds.get_movies_by_category("Drama")

        self.assertIsNone(result)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_categories_query_error(self, mock_connect):
        """
        Test get_all_categories returns empty list on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

        ds = DataSource()
        ds.connect()
        result = ds.get_all_categories()

        self.assertEqual(result, [])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_later_than_empty_result(self, mock_connect):
        """
        Test get_movies_later_than returns empty list if no movies found.
        """
        self.mock_cursor.fetchall.return_value = []
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_movies_later_than(2050)

        self.assertEqual(result, [])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movie_titles_by_actor_empty_result(self, mock_connect):
        """
        Test get_movie_titles_by_actor returns empty list if actor not found.
        """
        self.mock_cursor.fetchall.return_value = []
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_movie_titles_by_actor("Unknown Actor")

        self.assertEqual(result, [])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_3_filter_media_empty_filters(self, mock_connect):
        """
        Test get_3_filter_media returns empty list when no filters provided.
        """
        self.mock_cursor.fetchall.return_value = []
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_3_filter_media("", "", "")

        self.assertEqual(result, [])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_3_filter_media_query_error(self, mock_connect):
        """
        Test get_3_filter_media returns None on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")

        ds = DataSource()
        ds.connect()
        result = ds.get_3_filter_media("Actor A", "2020", "Thriller")

        self.assertIsNone(result)

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_media_from_title_normal(self, mock_connect):
        """
        Tests get_media_from_title under normal conditions.
        """
        self.mock_cursor.fetchall.return_value = [
            (
                'Movie',
                'Movie X',
                'Actor X',
                '1',
                'Genre X',
                'Movie about Actor X in Genre X.',
                'Platform X'
            ),
            (
                'Movie',
                'Movie Y',
                'Actor Y',
                '1',
                'Genre Y',
                'Movie about Actor Y in Genre Y.',
                'Platform Y'
            )
        ]
        ds = self.get_connected_datasource(mock_connect)
        result = ds.get_media_from_title('Movie X')
        self.assertEqual(
            result,
            (
                'Movie',
                'Movie X',
                'Actor X',
                '1',
                'Genre X',
                'Movie about Actor X in Genre X.',
                'Platform X'
            )
        )

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_media_from_title_query_error(self, mock_connect):
        """
        Tests get_media_from_title on query error.
        """
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query failed")
        ds = DataSource()
        ds.connect()
        result = ds.get_media_from_title('Movie Query')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
