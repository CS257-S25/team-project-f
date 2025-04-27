from flask import Flask, request
from ProductionCode import filter as filters
from ProductionCode.data import Data


app = Flask(__name__)
data = Data()


@app.route('/')
def homepage():
    """
    Determines the text on the homepage of the website. 
    Displays detailed instructions regarding the usage of the application.
    """
    return "StreamSearch</br></br>" \
    "To use this website, please insert the following into the address: /actor/category/year</br>" \
    "actor: The name of an actor to search for in a movie/show's cast.</br>" \
    "category: The category of movie/show to search for.</br>" \
    "year: The results will only include moves released on or after this year.</br></br>" \
    "IMPORTANT: All filters are optional. To omit a filter, replace it with " \
    "\"-\", \"_\", or \"x\".</br>" \
    "To represent spaces, either type the space normally, " \
    "or use \"-\", \"_\", or \"%20\".</br></br>" \
    "To view a list of categories available, insert /categories into the address."   


@app.route('/<actor>/<category>/<year>', strict_slashes=False)
def search_with_filters(actor, category, year):
    """
    Determines the text displayed on a page with the route /<actor>/<category>/<year>.
    Calls the filter_dataset function, which will return a string containing
    all the movies or TV shows which meet the filter criteria specified in the web address.
    Further information in these criteria is specified in homepage()'s return value.
    """
    return filters.filter_dataset(actor, category, year)

@app.route('/categories')
def list_categories():
    """
    Determines the text displayed on the page with the route /categories.
    Provides a list of all available category filters.
    """
    return f"Valid categories are as follows:</br></br>{filters.dataset.get_category_set()}"

@app.errorhandler(404)
def page_not_found(e):
    """
    Determines the text displayed on an unspecified route.
    Provides an error message and detailed instructions regarding proper use.
    """
    print(e)
    return "Error 404 - Incorrect format.</br></br>" \
    "To use this website, please insert the following into the address: /actor/category/year</br>" \
    "actor: The name of an actor to search for in a movie/show's cast.</br>" \
    "category: The category of movie/show to search for.</br>" \
    "year: The results will only include moves released on or after this year.</br></br>" \
    "IMPORTANT: All filters are optional. To omit a filter, replace it with " \
    "\"-\", \"_\", or \"x\".</br>" \
    "To represent spaces, either type the space normally, " \
    "or use \"-\", \"_\", or \"%20\".</br></br>" \
    "To view a list of categories available, insert /categories into the address."    

@app.errorhandler(500)
def python_bug(e):
    """
    Determines the text displayed if the program encounters a python bug.
    Provides an error message.
    """
    print(e)
    return "Error 500 - A python bug has occurred.</br></br>" \
    "Please check your input and try again."   




@app.route('/actor/<actor_name>')
def filter_by_actor(actor_name):
   """
   Filters media entries by actor name and formats the results
   """
   results = get_filtered_by_actor(actor_name)
   return format_media_results(results, f"actor: {actor_name}")


@app.route('/genre/<genre_name>')
def filter_by_genre(genre_name):
   """
   Filters media entries by genre and formats the results.
   """
   results = get_filtered_by_genre(genre_name)
   return format_media_results(results, f"genre: {genre_name}")




def get_filtered_by_actor(actor_name):
   """
   Uses the Filter class to filter media entries by actor name.
   """
   f = Filter(data)
   f.filter_by_actor(actor_name)
   return f.get_filtered_media_dict()


def get_filtered_by_genre(genre_name):
   """
   Uses the Filter class to filter media entries by genre.
   """
   f = Filter(data)
   f.filter_by_category(genre_name)
   return f.get_filtered_media_dict()


def format_media_results(results, label):
   """
   Formats a dictionary of media entries as text string.
   """
   if not results:
       return f"No entries found for {label}"


   lines = [f"Results for {label}"]
   for media in results.values():
       lines.append(f"- {media.title} ({media.release_year})")
   return "\n".join(lines)




if __name__ == "__main__":
   app.run()
