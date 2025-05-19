"""
Flask app for website.
"""

from flask import Flask, render_template, request
from ProductionCode.datasource import DataSource

app = Flask(__name__)
db = DataSource()

@app.route('/')
def homepage():
    """
    Determines the text on the homepage of the website. 
    Displays detailed instructions regarding the usage of the application.
    """
    return render_template("index.html")

@app.route('/actor/<name>', strict_slashes=False)
def search_by_actor(name):
    """
    Returns movie titles and descriptions featuring the specified actor.

    Args:
        name (str): The name of the actor to search for.

    Returns:
        str: A string listing matching movie titles and descriptions,
             or a message indicating no results were found.
    """
    try:
        results = db.get_movie_titles_by_actor(name)
        if not results:
            return f"No results found for actor: {name}"
        return "</br></br>".join(f"<b>{row[0]}</b> ({row[3]}): {row[1]}" for row in results)
    except LookupError as e:
        print("Lookup error in /actor route:", e)
        return f"Could not find actor: {name}"

@app.route('/year/<int:year>', strict_slashes=False)
def search_by_year(year):
    """
    Returns all movies released after the specified year.

    Args:
        year (int): The minimum release year for filtering movies.

    Returns:
        str: A string listing matching movies,
             or a message indicating no results were found.
    """
    try:
        results = db.get_movies_later_than(year-1)
        if not results:
            return f"No movies found released after {year}."
        return "</br></br>".join(f"<b>{row[0]}</b> ({row[3]}): {row[1]}" for row in results)
    except LookupError as e:
        print("Lookup error in /year route:", e)
        return f"Could not find titles after year: {year}"

@app.route('/category/<category>', strict_slashes=False)
def search_by_category(category):
    """
    Returns movie titles and descriptions in the specified category.

    Args:
        category (str): The genre or category of movies to search.

    Returns:
        str: A string listing matching movies,
             or a message indicating no results were found.
    """
    try:
        results = db.get_movies_by_category(category)
        if not results:
            return f"No movies found in category: {category}"
        return "</br></br>".join(f"<b>{row[0]}</b> ({row[3]}): {row[1]}" for row in results)
    except LookupError as e:
        print("Lookup error in /category route:", e)
        return f"Could not find movies in category: {category}"


@app.route('/filter', methods=['GET'])
def filter_form():
    """Renders genre selection form with dynamic dropdown."""
    categories = db.get_all_categories()
    return render_template('filter.html', categories=categories)

           ###### MEANT FOR SEARCHBAR WORK IN PROGRESS ######

@app.route('/filter/search', methods=['GET'])
def searchbar_results():
    title = request.args.get('title', '')
    titles = db.get_movie_by_title('title')
    return render_template('index_html', catgeories=categories)

           ###### MEANT FOR SEARCHBAR WORK IN PROGRESS ######

@app.route('/filter/results', methods=['GET'])
def filter_results():
    """Handles genre search and displays results."""
    category = request.args.get('category', '')
    actor = request.args.get('actor', '')
    year = request.args.get('year', '')

    #just category search
    if category != ''and actor=='' and year=='':
        results = db.get_movies_by_category(category)
        return render_template('filter_results.html', category=category, results=results)

    #just actor search
    if category ==''and actor!='' and year=='': 
        results = db.get_movie_titles_by_actor(actor)
        print("Results actor search:", results)
        print(type(results))
        return render_template('filter_results.html', actor=actor, results=results)
    
    #just year search
    if category ==''and actor=='' and year!='': 
        results = db.get_movies_later_than(str(int(year)-1))
        print("Results year search:")
        print(type(results))
        return render_template('filter_results.html', year=year, results=results)

    #Category, actor and year search (ALL THREE)
    if category !=''and actor!='' and year!='': 
        results = db.get_3_filter_media(actor, str(int(year)-1), category)
        print("Results all filters search:", results)
        print(type(results))
        return render_template('filter_results.html', actor = actor, year=year, category = category, results=results)

    #Category and actor search
    if category !=''and actor!='' and year=='': 
        results = db.get_3_filter_media(actor, 0, category)
        print("Results all filters search:", results)
        print(type(results))
        return render_template('filter_results.html', actor = actor, year=year, category = category, results=results)

    #Category and  year search
    if category !=''and actor=='' and year!='': 
        results = db.get_3_filter_media(actor, str(int(year)-1), category)
        print("Results all filters search:", results)
        print(type(results))
        return render_template('filter_results.html', actor = actor, year=year, category = category, results=results)

    # Actor and year search
    if category ==''and actor!='' and year!='': 
        results = db.get_3_filter_media(actor, str(int(year)-1), category)
        print("Results all filters search:", results)
        print(type(results))
        return render_template('filter_results.html', actor = actor, year=year, category = category, results=results)



@app.route('/about')
def about_page():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors for undefined routes.

    Args:
        e (HTTPException): The error object for the 404 error.

    Returns:
        tuple: An error message and HTTP status code 404.
    """
    print(e)
    return (
    "<h1>Error 404 - Wrong Format</h1></br></br>"
    "<p>Oops! The page you requested does not exist.</p>"
    "<p>Make sure your URL follows one of these formats:</p>"

    "[URL]/actor/Actor Name</br>"
    "[URL]/category/Category Name</br>"
    "[URL]/year/Year</br></br>"
    "<b>Here are some example URLs:</br></br>"
    "[URL]/actor/Emma Stone</br>"
    "[URL]/category/Comedy</br>"
    "[URL]/year/2010</br></br>"
    "<p><a href=\"/\">Click to return to the homepage</a></p>", 
    404)

@app.errorhandler(500)
def python_bug(e):
    """
    Handles 500 errors caused by unhandled exceptions in the application.

    Args:
        e (Exception): The error object for the 500 error.

    Returns:
        tuple: An error message and HTTP status code 500.
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
    app.run(port=5002)
