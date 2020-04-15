import requests
import app
from app import db
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
        

        #check what site to use
        if site == "TCGPlayer":

            #First Search(Find name [to make sure that it is the right name])
            nameSrc = soup.find_all("a", {"class": "product__name"})
            names = [] 
            for name in nameSrc:
                names.append(name.text)

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
                    priceSave = price.text
                    costs.append(float(priceSave.replace('$','')))
                    print(price.text)
        elif site == "CardKingdom":
            #First Search(Find name)
            nameSrc = soup.find_all("span", {"class": "productDetailTitle"})
            names = []
            for name in nameSrc:
               cardname=name.find_next("a")
               names.append(cardname.text)

            #Second Search(get version)
            versionsSrc = soup.find_all("div", {"class": "productDetailSet"})
            versions = []
            for version in versionsSrc:
                ver = version.find_next("a")
                versions.append(ver.text)

            #Third Search(get price)
            costs = [] 
            divs = soup.find_all("ul", {"class":"addToCartByType"})
            for div in divs:
                li = div.find_next("li", {"class":"itemAddToCart"})
                price = li.find_next("span", {"class":"stylePrice"})
                priceSave = price.text
                costs.append(float(priceSave.replace('$','')))

        else:
            print("ERROR: INVALID SITE")
        

        #Combined each argument together
        for x in range(len(versions)):
            print(names[x],versions[x],costs[x])
            #Check if card entry already exits
            if(Card.query.filter_by(cardName=names[x].lower()).filter_by(cardSet=versions[x]).all() == []):
                card = Card(cardName=names[x].lower(),cardSet=versions[x])
                db.session.add(card)
                db.session.commit()
            c = Card.query.filter_by(cardName=names[x].lower()).filter_by(cardSet=versions[x]).first()
            print(c)
            s = Site.query.filter_by(siteName=site).first()
            print(s.siteName)
            r = Results(price=costs[x],siteId=s.id, cardId=c.id)
            db.session.add(r)
            db.session.commit()




