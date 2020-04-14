import requests
import app
from app.models import Card, Site, Results
from bs4 import BeautifulSoup
from decimal import Decimal
#create link for searching tcgplayer from keyword and link to search results


class Search():
    def cardsearch(keyword,site):
        search = str(Site.query.filter_by(siteName=site).first())
        search = search + keyword
        print(search)
        result = requests.get(search)

        #print the status code (can be useful for testing when it can't connect)
        print(result.status_code)

    #put the results into the BeautifulSoup webscraping tool using the lxml tool
        src = result.content
        soup = BeautifulSoup(src, 'lxml')

    #First Search(Find name [to make sure that it is the right name])


    #Second search(get the versions of the cards and add them to array)
        versionsSRC = soup.find_all("a", {"class": "product__group"})
        versions = []
        for version in versionsSRC: 
            versions.append(version.text)

    #Third Search(get the cost and add it to array)
        costs = []
        divs = soup.find_all("div", {"class": "product__card"})
        for div in divs:
            prices = div.find_all("dd")
            for price in prices: 
                costs.append(price.text)
                print(price.text)
        

    #Combined each argument together
    #Will eventually get database.
        for x in range(len(versions)):
            print(versions[x],costs[x])
