"""Module for accessing and querying movie data from a PostgreSQL database."""

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

    def get_media_titles_only(self):
        """
        Fetches a full titles-only list of media from the database.
        For use in the searchbar in most webpages.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT title FROM stream_data
                ORDER BY title ASC
            ''')
            titles = []
            for title in cursor:
                titles.append("".join(title[0].splitlines()))
            return titles
        except psycopg2.DatabaseError as e:
            print("Something went wrong when executing the query:", e)
            return None

    def get_movies_later_than(self, release_year):
        """
        Fetches full info of movies released after the specified year.
        Args:
            release_year (int): The year to compare against.
        Returns:
            list of tuples: Movies released after the given year.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """SELECT *
            FROM stream_data WHERE release_year > %s ORDER BY release_year DESC"""
            cursor.execute(query, (release_year,))
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Something went wrong when executing the query:", e)
            return None

    def get_movie_titles_by_actor(self, actor_name):
        """
        Fetch movie titles where the given actor appears in the Casting field.
        Args:
            actor_name (str): Name of the actor to search for.
        Returns:
            list of tuples: Movie titles and descriptions featuring the actor.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """SELECT * FROM stream_data WHERE media_cast ILIKE %s"""
            cursor.execute(query, (f"%{actor_name}%",))
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Query failed:", e)
            return None

    def get_movies_by_category(self, category):
        """
        Fetches full info of movies by the specified category.
        Args:
            category (str): The category to filter movies by.
        Returns:
            list of tuples: Movies in the specified category.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """SELECT * FROM stream_data
              WHERE category ILIKE %s ORDER BY release_year DESC"""
            cursor.execute(query, (f"%{category}%",))
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Query failed:", e)
            return None

    def get_all_categories(self):
        """
        Fetches a sorted list of unique categories from the database.

        Returns:
            list of str: All distinct movie categories.
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = "SELECT category FROM stream_data WHERE category IS NOT NULL"
            cursor.execute(query)
            results = cursor.fetchall()

            genre_set = set()
            for row in results:
                genres = [genre.strip() for genre in row[0].split(",")]
                genre_set.update(genres)

            return sorted(genre_set)

        except psycopg2.DatabaseError as e:
            print("Query failed:", e)
            return []

    def get_3_filter_media(self, actor_name, release_year, category):
        """
        Fetches a sorted list of a unique actor, year, category from the database.

        Returns:
            list of str: All distinct movies from filter.

        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """
                    SELECT * FROM stream_data 
                    WHERE media_cast ILIKE %s 
                    AND category ILIKE %s 
                    AND release_year > %s 
                    ORDER BY release_year DESC
            """

            cursor.execute(query, (f"%{actor_name}%", f"%{category}%", release_year))
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Query failed:", e)
            return None
