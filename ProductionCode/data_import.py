import csv

def import_data():
    netflix_data = []
    amazon_prime_data = []
    disney_plus_data = []
    hulu_data = []

    # note: rows start at 1 because 0 is the headers
    with open("Data/netflix_titles.csv", encoding="utf-8") as csvfile:
        netflix_reader = csv.reader(csvfile)
        for row in netflix_reader:
            netflix_data.append(row)

    with open("Data/amazon_prime_titles.csv", encoding="utf-8") as csvfile:
        amazon_prime_reader = csv.reader(csvfile)
        for row in amazon_prime_reader:
            amazon_prime_data.append(row)

    with open("Data/disney_plus_titles.csv", encoding="utf-8") as csvfile:
        disney_plus_reader = csv.reader(csvfile)
        for row in disney_plus_reader:
            disney_plus_data.append(row)

    with open("Data/hulu_titles.csv", encoding="utf-8") as csvfile:
        hulu_reader = csv.reader(csvfile)
        for row in hulu_reader:
            hulu_data.append(row)
    return netflix_data, amazon_prime_data, disney_plus_data, hulu_data