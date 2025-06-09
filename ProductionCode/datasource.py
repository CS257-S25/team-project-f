"""
Module for accessing and querying movie data from a PostgreSQL database.
"""

import html
import psycopg2
import ProductionCode.psql_config as config


class DataSource:
    """Handles database connection and queries for movie data."""

    def __init__(self):
        """Constructor without immediate connection to the database."""
        self.connection = None

    def connect(self):
        """
        Initiates connection to database using credentials from psqlConfig.py.
        This method needs to be explicitly called to establish a connection.
        """
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    database=config.DATABASE,
                    user=config.USER,
                    password=config.PASSWORD,
                    host="localhost"
                )
            except psycopg2.DatabaseError as e:
                raise ConnectionError(f"Connection error: {e}") from e
        return self.connection

    def _execute_query(self, query, params=None):
        """
        Internal helper to execute queries and fetch results safely.

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters for query placeholders.

        Returns:
            list or tuple or None: Query result(s) or None on error.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print(f"Query failed: {e}")
            return None

    def get_media_later_than(self, release_year):
        """        
        Retrieves all movies released after a specified year.

        Args:
            release_year (int): The year to filter movies by.   
        Returns:
            list: A list of tuples containing movie data, or None if an error occurs.
        """
        query = """
            SELECT * FROM stream_data 
            WHERE release_year > %s 
            ORDER BY release_year DESC
        """
        return self._execute_query(query, (release_year,))

    def get_media_by_actor(self, actor_name):
        """
        Retrieves movie titles and descriptions for a specific actor.
        Args:
            actor_name (str): The name of the actor to filter movies by.
        Returns:
            list: A list of tuples containing movie titles and descriptions, 
            or None if an error occurs.
        """
        query = """
            SELECT * FROM stream_data 
            WHERE media_cast ILIKE %s
        """
        return self._execute_query(query, (f"%{actor_name}%",))

    def get_media_by_category(self, category):
        """
        Retrieves movies in a specific category or genre.
        Args:
            category (str): The genre or category to filter movies by.
        Returns:
            list: A list of tuples containing movie data, or None if an error occurs.
        """
        query = """
            SELECT * FROM stream_data 
            WHERE category ILIKE %s 
            ORDER BY release_year DESC
        """
        return self._execute_query(query, (f"%{category}%",))

    def get_all_categories(self):
        """
        Retrieves all unique categories from the database.
        Returns:
            list: A sorted list of unique categories, or an empty list if none found.
        """
        query = """
            SELECT category FROM stream_data WHERE category IS NOT NULL
        """
        results = self._execute_query(query)
        if results is None:
            return []

        genre_set = set()
        for row in results:
            genres = [genre.strip() for genre in row[0].split(",")]
            genre_set.update(genres)

        return sorted(genre_set)
    
    def get_media_by_advanced_filter(self, actor_name, release_year, category):
        """
        Retrieves media based on actor name, category, and release year.
        Args:
            actor_name (str): The name of the actor to filter by.
            release_year (int): The year to filter movies released after.
            category (str): The genre or category to filter movies by.
        Returns:
            list: A list of tuples containing media data, or None if an error occurs.
        """
        query = """
            SELECT * FROM stream_data 
            WHERE media_cast ILIKE %s 
            AND category ILIKE %s 
            AND release_year > %s 
            ORDER BY release_year DESC
        """
        return self._execute_query(query, (f"%{actor_name}%", f"%{category}%", release_year))

    def get_all_media_titles(self):
        """
        Retrieves all movie titles sorted by release year in descending order.
        Returns:
            list: A list of movie titles, or an empty list if none found.
        """
        query = """
            SELECT title, release_year FROM stream_data
            ORDER BY release_year DESC
        """
        results = self._execute_query(query)
        if results is None:
            return []

        titles = [html.unescape("".join(row[0].splitlines())) for row in results]
        return titles

    def get_all_actors(self):
        """
        Retrieves all unique actors from the database.
        Returns:
            list: A sorted list of unique actor names, or an empty list if none found.
        """
        query = """
            SELECT media_cast FROM stream_data WHERE media_cast IS NOT NULL
        """
        results = self._execute_query(query)
        if results is None:
            return []

        actor_set = set()
        for row in results:
            if row[0]:
                actors = [actor.strip() for actor in row[0].split(',')]
                actor_set.update(actors)

        return sorted(actor_set)

    def get_media_from_title(self, title):
        """
        Retrieves media data based on the title.
        Args:
            title (str): The title of the media to search for.
        Returns:
            tuple: A tuple containing media data if found, or None if not found.
        """
        query = """
            SELECT * FROM stream_data WHERE title ILIKE %s
        """
        result = self._execute_query(query, (title,))
        return result[0] if result else None
