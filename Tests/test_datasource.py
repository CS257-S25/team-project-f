"""
Unit tests for the DataSource class in ProductionCode.datasource.
Uses unittest and unittest.mock to simulate database behavior.
"""
import unittest
from unittest.mock import patch, MagicMock
import psycopg2

from ProductionCode.datasource import DataSource


class TestDataSource(unittest.TestCase):
    """Unit tests for the DataSource class methods."""

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movies_later_than(self, mock_connect):
        """Test getting movies released after a given year with valid result."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Movie A', 2022)]

        ds = DataSource()
        result = ds.get_movies_later_than(2020)
        self.assertEqual(result, [('Movie A', 2022)])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movies_later_than_empty_result(self, mock_connect):
        """Test getting movies with no results returned."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        ds = DataSource()
        result = ds.get_movies_later_than(2100)
        self.assertEqual(result, [])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movies_later_than_query_error(self, mock_connect):
        """Test behavior when a query error occurs."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.DatabaseError

        ds = DataSource()
        result = ds.get_movies_later_than(2020)
        self.assertIsNone(result)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movie_titles_by_actor(self, mock_connect):
        """Test retrieving movies by actor name."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Movie X', 'Actor Y')]

        ds = DataSource()
        result = ds.get_movie_titles_by_actor("Actor Y")
        self.assertEqual(result, [('Movie X', 'Actor Y')])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movie_titles_by_actor_empty_result(self, mock_connect):
        """Test actor name search with no results."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        ds = DataSource()
        result = ds.get_movie_titles_by_actor("Nonexistent Actor")
        self.assertEqual(result, [])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movie_titles_by_actor_query_error(self, mock_connect):
        """Test actor search with a query failure."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.DatabaseError

        ds = DataSource()
        result = ds.get_movie_titles_by_actor("Actor Y")
        self.assertIsNone(result)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_movies_by_category(self, mock_connect):
        """Test category-based movie search."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Movie B', '2021')]

        ds = DataSource()
        result = ds.get_movies_by_category("Comedy")
        self.assertEqual(result, [('Movie B', '2021')])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_all_categories(self, mock_connect):
        """Test extracting and deduplicating all genres/categories."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Action, Drama',), ('Comedy, Sci-Fi',)]

        ds = DataSource()
        result = ds.get_all_categories()
        self.assertEqual(result, ['Action', 'Comedy', 'Drama', 'Sci-Fi'])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_3_filter_media(self, mock_connect):
        """Test media filtering by actor, category, and release year."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Movie Z', 2023)]

        ds = DataSource()
        result = ds.get_3_filter_media("Actor Z", 2020, "Sci-Fi")
        self.assertEqual(result, [('Movie Z', 2023)])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_3_filter_media_empty_filters(self, mock_connect):
        """Test media filter query returning no matches."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        ds = DataSource()
        result = ds.get_3_filter_media("", 0, "")
        self.assertEqual(result, [])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_3_filter_media_query_error(self, mock_connect):
        """Test media filtering query with database error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.DatabaseError

        ds = DataSource()
        result = ds.get_3_filter_media("Actor X", 2000, "Action")
        self.assertIsNone(result)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_all_actors_normal(self, mock_connect):
        """Test deduplication and alphabetizing of actor names."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Actor A, Actor B',), ('Actor C, Actor D',)]

        ds = DataSource()
        result = ds.get_all_actors()
        self.assertEqual(result, ['Actor A', 'Actor B', 'Actor C', 'Actor D'])

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_media_from_title(self, mock_connect):
        """Test searching a movie by title."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('The Matrix', 1999)

        ds = DataSource()
        result = ds.get_media_from_title("Matrix")
        self.assertEqual(result, ('The Matrix', 1999))

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_media_from_title_normal(self, mock_connect):
        """Test normal media lookup by title with full data."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('Movie', 'Movie X', 'Actor X', '1', 'Genre X')

        ds = DataSource()
        result = ds.get_media_from_title("Movie X")
        self.assertEqual(result, ('Movie', 'Movie X', 'Actor X', '1', 'Genre X'))


if __name__ == '__main__':
    unittest.main()
