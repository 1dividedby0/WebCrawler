from BeautifulSoup import BeautifulSoup
import urllib2
import os.path

content_separator = "THISISASEPORATOR123"
tweet_separator = "THISISATWEETSEPARATOR569"

restaurants = open("restaurants.txt").read().split(",,,")

for restaurant in restaurants:
    print restaurant
    r = urllib2.urlopen('https://twitter.com/search?f=tweets&vertical=default&q=%23' + restaurant + '&src=typd').read()
    soup = BeautifulSoup(r)
    names = soup.findAll("span", {"class":"username js-action-profile-name"})
    tweets = soup.findAll("p", {"class":"TweetTextSize  js-tweet-text tweet-text"})
    ids = soup.findAll("li", {"class":"js-stream-item stream-item stream-item\n"})
    stream_size = len(names)
    if len(tweets) < len(names):
        stream_size = len(tweets)
    if len(ids) < len(tweets) or len(ids) < len(names):
        stream_size = len(ids)
    data = open(restaurant + ".txt").read().split(tweet_separator)

    f = open(restaurant + ".txt", "a")
    for i in range(stream_size):
        name = names[i].text
        tweet = tweets[i].text
        data_id = ids[i]["data-item-id"]
        new_tweet = True
        for m in data:
            if m.split(content_separator)[0] == data_id:
                new_tweet = False
        if new_tweet:
            biosoup = BeautifulSoup(urllib2.urlopen("https://twitter.com/" + name))
            bio = biosoup.find("p", {"class":"ProfileHeaderCard-bio u-dir"}).text
            f.write(tweet_separator + data_id.encode("utf-8") + content_separator + name.encode("utf-8") + content_separator + tweet.encode("utf-8") + content_separator + bio.encode("utf-8"))
