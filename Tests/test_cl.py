import unittest
import sys
from unittest.mock import patch
from io import StringIO
from ProductionCode import data as d
from ProductionCode import filter as f
import cl

data = d.Data()
filterset = f.Filter(data)
'''
class TestDataFunctions(unittest.TestCase):
    def setUp(self):
        """Load data and initialize the titles set based on the new structure."""
        netflix_dataset = "Dummy_data/dummy_netflix.csv"
        hulu_dataset = "Dummy_data/dummy_hulu.csv"
        amazon_dataset = "Dummy_data/dummy_amazon.csv"
        disney_dataset = "Dummy_data/dummy_disney.csv"

        data = d.Data()
        data.media_list = d.import_all_datasets_to_list(
            netflix_dataset=netflix_dataset,
            amazon_dataset=amazon_dataset,
            disney_dataset=disney_dataset,
            hulu_dataset=hulu_dataset
        )
        data.media_dict = d.create_media_dict_by_title(data.media_list)

        media_dict = data.get_media_dict()
'''
class TestFilterFunctions(unittest.TestCase):

    def setUp(self):
        global data
        global filterset

        netflix_dataset = "Dummy_data/dummy_netflix.csv"
        hulu_dataset = "Dummy_data/dummy_hulu.csv"
        amazon_dataset = "Dummy_data/dummy_amazon.csv"
        disney_dataset = "Dummy_data/dummy_disney.csv"

        data.media_list = d.import_all_datasets_to_list(
            netflix_dataset=netflix_dataset,
            amazon_dataset=amazon_dataset,
            disney_dataset=disney_dataset,
            hulu_dataset=hulu_dataset
        )
        data.media_dict = d.create_media_dict_by_title(data.media_list)

        filterset = f.Filter(data)

    def test_filter_by_actor(self):
        """Check if filtering by actor includes only correct titles."""
        filterset.filter_by_actor("Brendan Gleeson")
        self.assertEqual(filterset.filtered_media_dict, {"The Grand Seduction"})

    def test_filter_by_nonexistent_actor(self):
        """Check if filtering by a nonexistent actor results in an empty set."""
        filterset.filter_by_actor("Nonexistent Actor")
        self.assertEqual(filterset.filtered_media_dict, {})

    def test_filter_by_category(self):
        """Check if filtering by category includes only correct titles."""
        filterset.filter_by_category("Action")
        self.assertEqual(filterset.filtered_media_dict, {"The Grand Seduction"})
    def test_filter_by_category_lowercase(self):
        filterset.filter_by_category("horror")
        self.assertEqual(filterset.filtered_media_dict, {})
    def filter_by_category3(self):
        filterset.filter_by_category_uppercase("COMEDY")
        self.assertEqual(filterset.filtered_media_dict, {"Dick Johnson Is Dead"})
    def test_filter_by_nonexistent_category(self):
        filterset.filter_by_category("spiders")
        self.assertEqual(filterset.filtered_media_dict, {})

    def test_filter_by_year_onward_lower(self):
        filterset.filter_by_year_onward(1988)
        self.assertEqual(filterset.filtered_media_dict, "Ernest Saves Christmas")

    def test_filter_by_year_onward_higher(self):
        filterset.filter_by_year_onward(2021)
        
        self.assertEqual(filterset.filtered_media_dict, {
            "Ricky Velez: Here's Everything",
            "Blood & Water"
        })

class TestCommandLineArguments(unittest.TestCase):

    def setUp(self):
        global data
        global filterset
        self.mock_data = [
            [['s1', 'Movie', 'Title A', 'Director A', 'Actor X, Actor Y', 'USA', 'Jan 01, 2023', '2022', 'PG', '90 min', 'Action, Comedy', 'Description A', "Service A"]],
            [['s2', 'Show', 'Title B', 'Director B', 'Actor Y, Actor Z', 'UK', 'Feb 15, 2023', '2021', 'TV-MA', '2 Seasons', 'Drama, Sci-Fi', 'Description B', "Service B"]],
            [['s3', 'Movie', 'Title C', 'Director C', 'Actor X, Actor Z', 'Canada', 'Mar 20, 2023', '2023', 'G', '105 min', 'Comedy, Family', 'Description C', "Service C"]],
            [['s4', 'Show', 'Title D', 'Director E', 'Actor W, Actor X', 'USA', 'May 05, 2024', '2024', 'TV-Y', '3 Seasons', 'Action, Drama', 'Description E', "Service D"]],
        ]
        
        self.patcher = patch('ProductionCode.data.import_all_datasets_to_list', return_value=self.mock_data)
        self.mock_import = self.patcher.start()
        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output
        data.media_dict = d.create_media_dict_by_title(data.media_list)

    def tearDown(self):
        self.patcher.stop()
        sys.stdout = self.original_stdout

    def call_main_with_args(self, args):
        with patch('sys.argv', ['cl.py'] + args):
            cl.main()
        return self.captured_output.getvalue().strip().split('\n')

    def test_no_arguments(self):
        output = self.call_main_with_args([])
        self.assertEqual(sorted(['Title A', 'Title B', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_actor(self):
        output = self.call_main_with_args(['-a', 'Actor X'])
        self.assertEqual(sorted(['Title A', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_genre(self):
        output = self.call_main_with_args(['-c', 'Comedy'])
        self.assertEqual(sorted(['Title A', 'Title C']), sorted(output))

    def test_filter_by_year(self):
        output = self.call_main_with_args(['-y', '2022'])
        self.assertEqual(sorted(['Title A', 'Title C', 'Title D']), sorted(output))

    def test_filter_by_actor_and_genre(self):
        output = self.call_main_with_args(['-a', 'Actor X', '-g', 'Action'])
        self.assertEqual(sorted(['Title A', 'Title D']), sorted(output))

if __name__ == '__main__':
    unittest.main()
