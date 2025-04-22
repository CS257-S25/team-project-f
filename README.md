# CS257-F23-TeamTemplate
This is the repository for Team F's project.
The members of this team are: Eva, Maria, John, and Asa.

# StreamSearch CLI

## Overview

The StreamSearch CLI is a command-line application that allows users to explore a dataset of movies and shows from Netflix, Amazon Prime, Disney+, and Hulu. Users can filter the data by actor, genre, or release year to find titles of interest. The application is designed to be a simple and efficient way to query movie/show information directly from the command line.

## Features

* **Filter by Actor:** Find movies/shows featuring a specific actor.
* **Filter by Genre:** Find movies/shows belonging to a specific genre.
* **Filter by Release Year:** Find movies/shows released after a specific year.

## Usage

To use the Movie Browser CLI, open a terminal and navigate to the project's root directory. Then, use the following command structure:

```bash
python cl.py [options]


Options:
-a, --actor <actor_name>: Filters movies/shows by actor name.
Example: To find titles featuring "Leonardo DiCaprio":
python cl.py -a "Leonardo DiCaprio"


-g, --genre <genre_name>: Filters movies/shows by genre.
Example: To find titles in the "Drama" genre:
python cl.py -g "Drama"


-y, --year <release_year>: Filters movies/shows released after a specific year.
Example: To find titles released after 2000:
python cl.py -y 2000

```
## File Structure

```bash
team-project-f/
├── cl.py
├── ProductionCode/
│   └── data_setup.py
├── Tests/
│   └── test_cl.py
├── README.md
└── UserStories.md
```
cl.py: The main application script that parses command-line arguments and interacts with the ProductionCode.

ProductionCode/data_setup.py: Contains the logic for loading and processing the movie/show data.

Tests/test_cl.py: Contains the automated test suite for the cl.py application.

README.md: This file, providing an overview and usage instructions for the application.

UserStories.md: Contains the user stories and acceptance tests.

## Data Setup
The application loads movie/show data from CSV files (e.g., netflix.csv, hulu.csv, etc.). 

The ProductionCode/data_setup.py file handles the import and processing of this data into a usable format. 

The data is structured to allow for efficient filtering by actor, genre, and year. Dummy data is included in the Dummy_data/ directory for testing purposes.

## Testing
The application includes a comprehensive test suite to ensure its functionality and robustness. 

The tests cover various aspects of the application, including:

Command-line argument parsing

Data filtering logic

Correctness of output

To run the tests, execute the following command in the project's root directory:
```bash
python -m unittest Tests/test_cl.py
```


