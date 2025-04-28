"""
This file contains small functions to aid in formatting across various files.
"""

import re
from collections import OrderedDict

#Web Display
def make_list_web_displayable(a_list):
    """
    Returns a string containing each item in a list seperated by the 
    </br> tag for displaying on a website.
    """
    return '</br>'.join(a_list)

#def make_newline_list_web_displayable(a_list):
#    """
#    Replaces the newlines in a list and returns a string containing each item
#    in a list seperated by the </br> tag for displaying on a website.
#    """
#    for string in a_list:
#        string.replace("\n","</br>")
#    return make_list_web_displayable(a_list)


#Url Input
def url_input_not_null(search_term):
    """
    Checks whether an input parameter is not unused/"empty."
    """
    if search_term in {"_", "-", "x"}:
        return False
    return True

def reformat_url_input(search_string):
    """
    Ensures that input parameters contain spaces where necessary.
    """
    search_string = re.sub(r"%20|-|_", " ", search_string)
    return search_string.lower()


#Data Handling
def make_set(string):
    """
    Converts a comma-separated string into a set of values.
    """
    return set(string.split(", "))

def sort_dict_by_key(d):
    """
    Sorts a dictionary by its keys and returns an OrderedDict.
    """
    return OrderedDict(sorted(d.items()))
