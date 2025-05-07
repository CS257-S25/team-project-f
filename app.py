"""
Flask app for website.
"""

from flask import Flask
from ProductionCode.datasource import DataSource

app = Flask(__name__)
db = DataSource()

@app.route('/')
def homepage():
    """
    Determines the text on the homepage of the website. 
    Displays detailed instructions regarding the usage of the application.
    """
    return """
    <h1>Welcome to StreamSearch</h1></br></br>
    StreamSearch helps you find movies and TV shows based on actor names, categories, and release years.</br></br>
    <b>How to Use StreamSearch:</b></br>
    - <b>Actor</b>: Enter the name of an actor to find movies or shows they appear in. </br>
    - <b>Category</b>: Search by genre or category (e.g., Comedy, Action, Drama). </br>
    - <b>Year</b>: Filter results to show movies or shows released on or after a specified year.</br></br>
    
    <b>Example URLs:</b></br>
    - /actor/Emma Stone</br>
    - /category/Comedy</br>
    - /year/2010</br></br>"""

@app.route('/actor/<name>', strict_slashes=False)
def search_by_actor(name):
    """
    Route that returns movie titles and descriptions featuring the specified actor.
    """
    try:
        results = db.get_movie_titles_by_actor(name)
        if not results:
            return f"No results found for actor: {name}"
        return "</br></br>".join(f"<b>{title}</b>: {desc}" for title, desc in results)
    except LookupError as e:
        print("Lookup error in /actor route:", e)
        return f"Could not find actor: {name}"

@app.route('/year/<int:year>', strict_slashes=False)
def search_by_year(year):
    """
    Route that returns all movies released after the specified year.
    """
    try:
        results = db.get_movies_later_than(year)
        if not results:
            return f"No movies found released after {year}."
        return "</br></br>".join(f"<b>{row[0]}</b> ({row[3]}): {row[1]}" for row in results)
    except LookupError as e:
        print("Lookup error in /year route:", e)
        return f"Could not find titles after year: {year}"

@app.route('/category/<category>', strict_slashes=False)
def search_by_category(category):
    """
    Route that returns movie titles and descriptions in the specified category.
    """
    try:
        results = db.get_movies_by_category(category)
        if not results:
            return f"No movies found in category: {category}"
        return "</br></br>".join(f"<b>{row[0]}</b> ({row[3]}): {row[1]}" for row in results)
    except LookupError as e:
        print("Lookup error in /category route:", e)
        return f"Could not find movies in category: {category}"

@app.errorhandler(404)
def page_not_found(e):
    """
    Determines the text displayed on an unspecified route.
    Provides an error message and detailed instructions regarding proper use.
    """
    print(e)
    return (
        "Error 404 - Incorrect format.</br></br>"
        "To use this website, please insert the following "
        "into the address: /actor/category/year</br>"
        "actor: The name of an actor to search for in a movie/show's cast.</br>"
        "category: The category of movie/show to search for.</br>"
        "year: The results will only include moves released on or after this year.</br></br>"
        "IMPORTANT: All filters are optional. To omit a filter, replace it with "
        "\"-\", \"_\", or \"x\".</br>"
        "To represent spaces, either type the space normally, "
        "or use \"-\", \"_\", or \"%20\".</br></br>"
        "To view a list of categories available, insert /categories into the address.",
        404)

@app.errorhandler(500)
def python_bug(e):
    """
    Determines the text displayed if the program encounters a python bug.
    Provides an error message.
    """
    print(e)
    return (
        "Error 500 - A python bug has occurred.</br></br>"
        "Please check your input and try again.",
        500)

@app.route('/cause_500')
def cause_500():
    """
    Force a 500 error
    """
    raise RuntimeError("Test exception to trigger 500 error")

if __name__ == "__main__":
    app.run()
