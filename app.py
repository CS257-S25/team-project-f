"""
Flask app for website.
"""

from flask import Flask, render_template, request
from ProductionCode.datasource import DataSource

app = Flask(__name__)
ds = DataSource()

@app.route('/')
def homepage():
    """
    Determines the text on the homepage of the website. 
    Displays detailed instructions regarding the usage of the application.
    """
    return render_template(
        "index.html",
        titles=ds.get_media_titles_only()
    )

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
        results = ds.get_movie_titles_by_actor(name)
        if not results:
            return f"No results found for actor: {name}"
        return "</br></br>".join(f"<b>{row[1]}</b> ({row[3]}): {row[5]}" for row in results)
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
        results = ds.get_movies_later_than(year-1)
        if not results:
            return f"No movies found released after {year}."
        return "</br></br>".join(f"<b>{row[1]}</b> ({row[3]}): {row[5]}" for row in results)
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
        results = ds.get_movies_by_category(category)
        if not results:
            return f"No movies found in category: {category}"
        return "</br></br>".join(f"<b>{row[1]}</b> ({row[3]}): {row[5]}" for row in results)
    except LookupError as e:
        print("Lookup error in /category route:", e)
        return f"Could not find movies in category: {category}"

@app.route('/filter', methods=['GET'])
def filter_form():
    """
    Renders genre selection form with dynamic dropdown.
    """
    categories, actors, titles = [], [], []
    try:
        categories = ds.get_all_categories()
        actors = ds.get_all_actors()
        titles = ds.get_media_titles_only()
    except Exception as e:
        print("Error in /filter:", e)

    return render_template(
        'filter.html',
        categories=categories,
        actors=actors,
        titles=titles
    )


@app.route('/filter/results', methods=['GET'])
def filter_results():
    """
    Handles advanced filter search and displays results.
    """
    category = request.args.get('category', '')
    actor = request.args.get('actor', '')
    year = request.args.get('year', '')

    results, titles = [], []
    try:
        results = ds.get_3_filter_media(
            actor if actor else '',
            str(int(year) - 1) if year else '0',
            category if category else ''
        )
    except Exception as e:
        print("Error in /filter/results query:", e)

    try:
        titles = ds.get_media_titles_only()
    except Exception as e:
        print("Error getting titles in /filter/results:", e)

    return render_template(
        'filter_results.html',
        actor=actor,
        year=year,
        category=category,
        results=results,
        titles=titles
    )


@app.route('/about')
def about_page():
    """
    Renders the about page with information about the application.
    """
    titles = []
    try:
        titles = ds.get_media_titles_only()
    except Exception as e:
        print("Error in /about:", e)

    return render_template(
        'about.html',
        titles=titles
    )


@app.route('/search', methods=['GET'])
def search_result_page():
    """
    Renders the search result page given an individual movie.
    """
    title_choice = request.args.get('title_choice', '')
    media, titles = None, []

    try:
        media = ds.get_media_from_title(title_choice)
    except Exception as e:
        print("Error getting media from title:", e)

    try:
        titles = ds.get_media_titles_only()
    except Exception as e:
        print("Error getting titles in /search:", e)

    return render_template(
        'search_result.html',
        titles=titles,
        media=media
    )


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors for undefined routes.
    """
    print("404 error:", e)
    titles = []
    try:
        titles = ds.get_media_titles_only()
    except Exception as err:
        print("Error getting titles in 404 handler:", err)

    return render_template(
        '404.html',
        titles=titles
    ), 404


@app.errorhandler(500)
def python_bug(e):
    """
    Handles 500 errors and logs error details.
    """
    print("500 error:", e)
    titles = []
    try:
        titles = ds.get_media_titles_only()
    except Exception as err:
        print("Error getting titles in 500 handler:", err)

    return render_template(
        '500.html',
        titles=titles
    ), 500


@app.route('/cause_500')
def cause_500():
    """
    Force a 500 error
    """
    raise RuntimeError("Test exception to trigger 500 error")

if __name__ == "__main__":
    app.run(port=5134)
    #app.run(port=5150, host='0.0.0.0', debug=False)
