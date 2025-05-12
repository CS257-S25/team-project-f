"""Module for accessing and querying movie data from a PostgreSQL database."""

import psycopg2
import ProductionCode.psql_config as config

class DataSource:
    """Handles database connection and queries for movie data."""

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        """
        Initiates connection to database using credentials from psql_config.py.
        """
        try:
            connection = psycopg2.connect(
                database=config.DATABASE,
                user=config.USER,
                password=config.PASSWORD,
                host="localhost"
            )
        except psycopg2.DatabaseError as e:
            raise ConnectionError(f"Connection error: {e}") from e
        return connection
 
    def get_movies_later_than(self, release_year):
        """
        Fetches full info of movies released after the specified year.
        Args:
            release_year (int): The year to compare against.
        Returns:
            list of tuples: Movies released after the given year.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM stream_data WHERE release_year > %s ORDER BY release_year DESC"
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
            query = "SELECT title, media_description FROM stream_data WHERE media_cast ILIKE %s"
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
            query = "SELECT * FROM stream_data WHERE category ILIKE %s ORDER BY release_year DESC"
            cursor.execute(query, (f"%{category}%",))
            return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Query failed:", e)
            return None
