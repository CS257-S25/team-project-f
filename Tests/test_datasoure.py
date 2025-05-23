import unittest
from unittest.mock import patch, MagicMock
from ProductionCode.datasource import DataSource

class TestDataSource(unittest.TestCase):

    def setUp(self):
        # Create a reusable mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Test connect() establishes a connection and returns it."""
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        conn = ds.connect()

        self.assertEqual(conn, self.mock_conn)
        mock_connect.assert_called_once()

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_later_than(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [('Movie A', 2022)]
        mock_connect.return_value = self.mock_conn

        ds = DataSource()
        ds.connect()
        result = ds.get_movies_later_than(2020)

        self.assertEqual(result, [('Movie A', 2022)])
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT *
            FROM stream_data WHERE release_year > %s ORDER BY release_year DESC""",
            (2020,)
        )

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movie_titles_by_actor(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [('Movie X', 'Actor Y')]
        mock_connect.return_value = self.mock_conn

        ds = DataSource()
        ds.connect()
        result = ds.get_movie_titles_by_actor("Actor Y")

        self.assertEqual(result, [('Movie X', 'Actor Y')])
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM stream_data WHERE media_cast ILIKE %s",
            ("%Actor Y%",)
        )

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_movies_by_category(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [('Movie B', '2021')]
        mock_connect.return_value = self.mock_conn

        ds = DataSource()
        ds.connect()
        result = ds.get_movies_by_category("Horror")

        self.assertEqual(result, [('Movie B', '2021')])
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT * FROM stream_data
              WHERE category ILIKE %s ORDER BY release_year DESC""",
            ("%Horror%",)
        )

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_categories(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [("Action, Drama",), ("Comedy",), ("Drama, Sci-Fi",)]
        mock_connect.return_value = self.mock_conn

        ds = DataSource()
        ds.connect()
        result = ds.get_all_categories()

        self.assertEqual(result, ['Action', 'Comedy', 'Drama', 'Sci-Fi'])

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_3_filter_media(self, mock_connect):
        self.mock_cursor.fetchall.return_value = [('Movie Z', 2023)]
        mock_connect.return_value = self.mock_conn

        ds = DataSource()
        ds.connect()
        result = ds.get_3_filter_media("Actor A", "2020", "Thriller")

        self.assertEqual(result, [('Movie Z', 2023)])
        self.mock_cursor.execute.assert_called_once_with(
            """
                    SELECT * FROM stream_data 
                    WHERE media_cast ILIKE %s 
                    AND category ILIKE %s 
                    AND release_year > %s 
                    ORDER BY release_year DESC
            """,
            ("%Actor A%", "%Thriller%", "2020")
        )

if __name__ == '__main__':
    unittest.main()
