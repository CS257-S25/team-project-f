# CS257-F23-Team
This is the repository for Team F's project.
The members of this team are: Eva, Maria, John, and Asa.

# Option A: Code Design Improvements

## Code Smell/Naming Issue 1: Repetitive Database Connection Logic

- **Type of issue**: Code Smell – *Dispensables / Duplicate Code* *Bloaters / Long Method*
- **Location**: `ProductionCode/datasource.py`, lines 31–58
- **What we did**:  
  Refactored the repeated database connection logic into a private `_ensure_connection()` method to ensure connection establishment happens uniformly before each query. Reduced long methods by delegating to helper. This improves maintainability and removes duplicated logic.

## Code Smell/Naming Issue 2: [INSERT TITLE]

- **Type of issue**:
- **Location**:
- **What we did**:  

---

# Option B: Front-End Design Improvements

## Usability Issue 1: Autocomplete for Search Bar

- **Issue**: The autocompletion for the search bar was not working, making it harder for users to find valid actor names.
- **Page**: `templates/filter.html`
- **What we did**:  
  Implemented.... This allows users to see suggestions as they type, improving search efficiency and experience.

## Usability Issue 2: Limited Search Results Display

- **Issue**: Movie results on the `/filter_results` page were very limited. If users wanted to see more detailed information such as the entire cast, they had no way to access it.
- **Page**: `templates/results.html`
- **What we did**:  
  Enhanced the results display to include more information such as full cast, ...


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
## Scanability
The webpage features clear headers and a consistently placed navigation bar, which enables users to quickly identify the app’s name and easily locate key sections that support various functionalities. The uniform placement of the navigation bar across all pages allows users to scan and navigate between different areas of the site. Functionalities are organized into concise, well-spaced subsections with intuitive labels, helping users grasp key options such as filtering movies by genre, actor, or year.

## Satisficing
Input fields for actor name and year, along with the genre selection dropdown, are designed to be simple and intuitive, allowing users to interact immediately without additional instructions. Familiar design conventions—like a traditional navigation bar, tiles that change color or outline on hover, and underlined clickable links—make the interface predictable and clearly indicate interactive elements. This reduces cognitive load by guiding users smoothly through the process. If a user makes an incorrect filter choice, the easily accessible "Back to Search" link at the bottom of the page allows quick recovery.

## Muddling through
The navigation bar and form elements are self-explanatory, encouraging users to jump in and explore without needing detailed guidance. Furthermore, accessibility considerations such as matching id and label tags on form inputs enhance usability for those navigating with screen readers or keyboards, ensuring a more inclusive user experience.


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

    404.html: Page loaded when user attempts to load a page that cannot be found.

    500.html: Page loaded when a bug occurs. Prompts redirect to homepage.

    genre_results.html: Displays results of search in genre.html.

    genre.html: Page to filter movies by genre.

    index.html: Homepage of the website.

    results.html: Functions with the command line application.

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
