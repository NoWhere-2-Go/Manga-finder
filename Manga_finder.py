from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_lang():
    valid = False
    languages = ["english", "spanish", "japanese", "german", "french", "italian", "russian", "chinese", "korean"]

    # check if language user typed is valid
    while not valid:
        lang = input("What language are you looking for? ")
        for langs in languages:
            if langs == lang.lower():
                return lang
        print("Enter a valid language")
        
def get_price_min():
    price = int(input("What is your minimum price? "))
    while price < 0:
        print("Enter a valid price")
        price = int(input("What is your minimum price? "))
    return price


def get_price_max(minimum):
    price = int(input("What is your maximum price? "))
    while price <= minimum:
        print("Enter a valid price")
        price = int(input("What is your maximum price? "))
    return price


if __name__ == "__main__":
    manga = input("What manga do you want to search for? ")
    language_preference = get_lang()
    min_price = get_price_min()
    max_price = get_price_max(min_price)


    ebay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={manga}+manga+{language_preference}&_png=1&_udlo={min_price}&_udhi={max_price}"
    page = requests.get(ebay_url).text
    soup = BeautifulSoup(page, "html.parser")

    # make sure to scrape every page that has manga listings
    x = 1
    manga_listings = []

    while x <= 3:
        x = x + 1
        ebay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={manga}+manga+{language_preference}&_png={x}&_udlo={min_price}&_udhi={max_price}"
        title_tags = soup.find_all('h3', class_='s-item__title')
        price_tags = soup.find_all('span', class_='s-item__price')

        # lets store all manga listings inside a list
        for i in range(1, len(title_tags)):
            manga_listings.append({'Title': title_tags[i].text, 'Price': float(price_tags[i].text[1:])})

    # write the list into a pandas dataframe
    sorted_manga_listings = sorted(manga_listings, key=lambda d: d['Price'])
    print(*sorted_manga_listings, sep='\n')
    df = pd.DataFrame.from_dict(manga_listings)
    df.sort_values(by="Price")
    df.to_csv("ebay_manga_postings.csv")
