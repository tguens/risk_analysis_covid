"""
File to gather helper functions for the scrapping
of information sources.
"""

from bs4 import BeautifulSoup
import requests
import sys
import json

#===================================================
#================= A first set of helper functions to scrap tweeter data"

def get_tweet_text(tweet):
    tweet_text_box = tweet.find(
        "p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all(
        "a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')

    return tweet_text


def get_this_page_tweets(soup):
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue
            #ignore if there is any loading or tweet error

        if tweet_data:
            tweets_list.append(tweet_data)
            print(".", end="")
            sys.stdout.flush()
    print(tweets_list)
    return tweets_list


def get_tweets_data(username, soup):
    tweets_list = list()
    tweets_list.extend(get_this_page_tweets(soup))
    return tweets_list


def dump_data(username, tweets, root='../data/'):
    filename = root + username+"_twitter.json"
    print("\nDumping data in file " + filename)
    data = dict()
    data["tweets"] = tweets
    with open(filename, 'w') as fh:
        fh.write(json.dumps(data))

    return filename


def test_scrap():
    username = "Macky_Sall"
    url = "http://www.twitter.com/" + username
    print("\n\nDownloading tweets for " + username)
    response = None
    try:
        response = requests.get(url)
    except Exception as e:
        print(repr(e))
        sys.exit(1)
    print(response)

    soup = BeautifulSoup(response.text, 'html')
    tweets = get_tweets_data(username, soup)
    print(tweets)
    dump_data(username, tweets, )

if __name__ == "__main__":
    test_scrap()