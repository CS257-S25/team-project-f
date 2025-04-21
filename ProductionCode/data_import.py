import csv

def import_data(
    netflix_path="Data/netflix_titles.csv",
    amazon_path="Data/amazon_prime_titles.csv",
    disney_path="Data/disney_plus_titles.csv",
    hulu_path="Data/hulu_titles.csv"
):
    netflix_data = []
    amazon_prime_data = []
    disney_plus_data = []
    hulu_data = []

    with open(netflix_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            netflix_data.append(row)

    with open(amazon_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            amazon_prime_data.append(row)

    with open(disney_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            disney_plus_data.append(row)

    with open(hulu_path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            hulu_data.append(row)

    return netflix_data, amazon_prime_data, disney_plus_data, hulu_data