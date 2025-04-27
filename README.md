# CS257-F23-TeamTemplate
This is the repository for Team F's project.
The members of this team are: Eva, Maria, John, and Asa.

# StreamSearch CLI

## Overview

The StreamSearch CLI is a command-line application that allows users to explore a dataset of movies and shows from Netflix, Amazon Prime, Disney+, and Hulu. Users can filter the data by actor, category, or release year to find titles of interest. The application is designed to be a simple and efficient way to query movie/show information directly from the command line.

## Features

* **Filter by Actor:** Find movies/shows featuring a specific actor.
* **Filter by Category:** Find movies/shows belonging to a specific category.
* **Filter by Year Onward:** Find movies/shows released after/during a specific year.

## Usage

To use the StreamSearch CLI, open a terminal and navigate to the project's root directory. Then, use the following command structure:

```bash
python cl.py <options>

Options:
-a, --actor <actor_name>: Filters movies/shows by actor name.
Example: To find titles featuring "Leonardo DiCaprio":
python cl.py -a "Leonardo DiCaprio"


-c, --category <category_name>: Filters movies/shows by category.
Example: To find titles in the "Drama" category:
python cl.py -c "Drama"


-y, --year <year>: Filters movies/shows released after/during a specific year.
Example: To find titles released from 2000 onwards:
python cl.py -y 2000

```
## File Structure

```bash
team-project-f/
├── cl.py
├── ProductionCode/
│   └── data.py
│   └── filter.py
├── Tests/
│   └── test_cl.py
├── README.md
└── UserStories.md
```
cl.py: The main application script that parses command-line arguments and interacts with the ProductionCode.

ProductionCode/data.py: Contains the logic for loading and processing the movie/show data.

ProductionCode/filter.py: Contains the logic for filtering the movie/show data based on user input.

Tests/test_cl.py: Contains the automated test suite for the cl.py application.

README.md: This file, providing an overview and usage instructions for the application.

UserStories.md: Contains the user stories and acceptance tests.

## Data Setup
The application loads streaming service movie/show data from CSV files (e.g., netflix.csv, hulu.csv, etc.). The ProductionCode/data.py file handles the importing and processing of this data into a usable format. The data is structured to allow for efficient filtering by actor, genre, and year via the filter.py file. Dummy data is included in the Dummy_data/ directory for testing purposes.

## Testing
The application includes a comprehensive test suite to ensure its functionality and robustness. 

The tests cover various aspects of the application, including:

* Command-line argument parsing
* Data filtering logic
* Correctness of output

To run the tests, execute the following command in the project's root directory:
```bash
python -m unittest Tests/test_cl.py
```

## Running the Flask App
