# CS257-F23-TeamTemplate
This is the repository for Team F's project.
The members of this team are: Eva, Maria, John, and Asa.

# StreamSearch CLI

## Overview

The StreamSearch CLI is a command-line application that allows users to explore a dataset of movies and shows from Netflix, Amazon Prime, Disney+, and Hulu. Users can filter the data by actor, category, or release year to find titles of interest.

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

# StreamSearch Flask App

## Overview

The **StreamSearch Flask App** is a simple web application that allows users to explore our dataset of movies and shows from popular streaming platforms.

## Features

* **Filter by Actor:** Find movies/shows featuring a specific actor.
* **Filter by Category:** Find movies/shows belonging to a specific genre/category.
* **Filter by Year:** Find movies/shows released on or after a specific year.
* **List Categories:** View a list of all available categories to filter by.
* **Friendly Error Handling:** Displays a helpful message for incorrect URLs or queries.

## Usage

Start the app by running the following command:

```bash
python app.py
```

Access the app by opening your browser and navigating to the URL provided. The application provides two main routes for filtering content.

### Homepage
Displays detailed instructions on how to use the app.  

### Filter by Actor (Route 1)
Filters media entries based on actor.
**URL:** `[URL]/actor/<actor name>`

**Example:** To find titles that Emma Stone acts in:

```text
[URL]/actor/Emma%Stone
```


### Filter by Category (Route 2)
Filters media entries based on category.
**URL:** `[URL]/category/<category name>`

**Example:** To find titles in the Comedy category:

```text
[URL]/category/Comedy
```


### Filter by Year (Route 3)
Filters media entries based on year.
**URL:** `[URL]/year/<year>`

**Example:** To find titles released after 2010:

```text
[URL]/year/2010
```


## File Structure

```bash
team-project-f/
├── cl.py
├── app.py
├── ProductionCode/
│   ├── data.py
│   ├── datasource.py
│   ├── filtering.py
│   ├── formatting.py
│   └── psql_config.py
├── static/
│   └── stylesheet.css
├── templates/
│   ├── 404.html
│   ├── 500.html
│   ├── genre_results.html
│   ├── genre.html
│   ├── index.html
│   └── results.html
├── Tests/
│   ├── test_cl.py
│   └── test_app.py
├── Data/
│   ├── amazon_prime_titles.csv
│   ├── disney_plus_titles.csv
│   ├── hulu_titles.csv
│   ├── netflix_titles.csv
│   └── metadata.md
├── README.md
├── Contract.md
├── Proposal.md
└── UserStories.md
```
cl.py: The command-line application script that parses command-line arguments and interacts with the ProductionCode.
app.py: The script responsible for running the website application.
ProductionCode/
    data.py: Contains the logic for loading and processing the movie/show data.
    datasource.py: Module for accessing and querying movie data from a PostgreSQL database.
    filtering.py: Contains the logic for filtering the movie/show data based on user input.
    formatting.py: Contains logic for miscellaneous reformatting needed in various locations.
    psql_config: Contains login information to access the databases. Assumed to exist by datasource.py, ignored in .gitignore
static/
    stylesheet.css: Default stylesheet loaded in all HTML pages.
templates/
    404.html:
    500.html:
    genre_results.html:
    genre.html:
    index.html: Homepage of the website.
    results.html: 
Tests/
    test_cl.py: Contains the automated test suite for the cl.py application.
    test_app.py: Contains the automated test suite for the app.py application.
Data/
    metadata.md: Contains information on amazon_prime_titles.csv, disney_plus_titles.csv, hulu_titles.csv, and netflix_titles.csv. Refer there for information on each of those files.
README.md: This file, providing an overview and usage instructions for the application.
Proposal.md: Contains a proposal for what this project will be about.
Contract.md: Contains the contract to ensure stability and deliverability in the group as we work together.
UserStories.md: Contains the necessary user stories and acceptance tests.

## Data Setup
The application loads streaming service movie/show data from CSV files (e.g., netflix.csv, hulu.csv, etc.). The ProductionCode/data.py file handles the importing and processing of this data into a usable format. The data is structured to allow for efficient filtering by actor, genre, and year via the filtering.py file. Dummy data is included in the Dummy_data/ directory for testing purposes.

## Testing
The application includes a comprehensive test suite to ensure its functionality and robustness. 
To run the test for command-line argument, execute the following command in the project's root directory:
```bash
python -m unittest Tests/test_cl.py
```
To run the test for the Flask app, execute the following command in the project's root directory:
```bash
python -m unittest Tests/test_app.py
```
