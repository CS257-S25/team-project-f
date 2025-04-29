"""
Flask app for website.
"""

from flask import Flask
from ProductionCode.filtering import Filter
from ProductionCode.data import Data

app = Flask(__name__)
dataset = Data()
filtering = Filter(dataset)

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
    filtered_data = filtering.filter_for_web(actor, category, year)
    return filtered_data.get_web_displayable_titles()

@app.route('/categories')
def list_categories():
    """
    Determines the text displayed on the page with the route /categories.
    Provides a list of all available category filters.
    """
    return f"Valid categories are as follows:</br></br>{dataset.get_category_set()}"

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

@app.route('/cause_500')
def cause_500():
    """
    Force a 500 error
    """
    raise RuntimeError("Test exception to trigger 500 error")

if __name__ == "__main__":
    app.run()
