from bs4 import BeautifulSoup
import urllib

price = "&attrs=RestaurantsPriceRange2.1"
rfile = open("restaurants.txt")
restaurants = rfile.read().split(',,,')
rfile.close()

wfile = open("restaurants.txt", "w")
for i in range(1, 5):
    if i != 1:
        price += "RestaurantsPriceRange2." + str(i)
    # use range instead of xrange with python 3
    for j in range(0,990,10):

        soup = BeautifulSoup(urllib.request.urlopen("https://www.yelp.com/search?find_desc=Restaurants&find_loc=CA&start=" + str(j) + price).read())

        stream = soup.find_all("a", {"class":"biz-name js-analytics-click"})
        if len(stream) == 0:
            print(soup.prettify())
            break

        for k in range(len(stream)):
            name = stream[k].find('span').contents[0]
            # it's an ad
            if k == 0:
                continue
            if name not in restaurants:
                name = name.replace(" ", "")
                name = name.replace("&amp;", "and")
                name = name.replace("\'", "")
                restaurants.append(name)
                print(name)
            elif name in restaurants:
                print("Smoothly Running")

for i in range(len(restaurants)):
    restaurants[i] = restaurants[i].encode("utf-8")

wfile.write(',,,'.join(restaurants))
