"""
File to gather helper functions for the scrapping
of information sources.

Useful link: 
http://www.africain.info/afrique-tous-les-journaux-africains
"""

from bs4 import BeautifulSoup
import requests
import sys
import json
import newspaper
import tqdm
from newspaper import Article
from sources import sources, header
import subprocess


#=======================================================
# A first set of helper functions to scrap tweeter data"

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


#=======================================================
# Helper functions to scrap newspapers

'''
class ArticleScrapper:
    def __init__(self, 
                country: str, 
                source: str,
                website:str, 
                language="fr"):
        self.country = country
        self.language = language
        self.source = source
        self.website = website
        self.counter = 0
        self.header = header

    def create_id(self, article):
        _id = "{}_{}_{}".format(self.country, self.source, self.counter)
        self.counter +=1
        return _id
        
    def read_article(self, url):
        # TODO: Make sure we can read the article (tests?)
        # TODO: Assign id smartly
        # TODO Make sure we have a clear formatting for the date
        article = Article(url, language=self.language)
        article.download()
        article.parse()

        _id = self.create_id(article)
        if article.publish_date is None:
            _date = self.get_date(article)
        else:
            _date = article.publish_date

        out_article = [_id, article.title,
                       article.text,
                       _date,
                       self.country,
                       self.source]
        return out_article, header

    def read_all(self, max_iter=10):
        """
        Get list of lists of articles.
        """
        config = newspaper.Config()
        config.memoize_articles = False
        paper = newspaper.build(self.website, 
                                language=self.language,
                                config=config) 
        articles = []
        iter_ = 0
        print("PAPER", paper.articles)
        for article in tqdm.tqdm(paper.articles):
            print("URL:", article.url)
            row, _ = self.read_article(article.url)
            articles.append(row)
            iter_ += 1
            if iter_ > max_iter:
                break
        return articles, header

  class ArticleScrapper:
    def __init__(self, 
                country: str, 
                source: str,
                website:str, 
                language="fr"):
        self.country = country
        self.language = language
        self.source = source
        self.website = website
        self.counter = 0
        self.header = header

    def create_id(self, article):
        _id = "{}_{}_{}".format(self.country, self.source, self.counter)
        self.counter +=1
        return _id
        
    def get_date(self, article): 
        #TODO: Make it more automatic and precise.
        soup = BeautifulSoup(article.html, 'html.parser')
        try:
            date_text = soup.find_all("div", class_='date')[0]
            text = date_text.get_text()
            return text[:14] #Heuristic. need cleaning up.
        except:
            return 'Unknown'

    def read_article(self, tweet, url):
        # TODO: Make sure we can read the article (tests?)
        # TODO: Assign id smartly
        # TODO Make sure we have a clear formatting for the date
        article = Article(url, language=self.language)
        article.download()
        article.parse()
        _id = self.create_id(article)
        out_article = [_id, 
                       article.title,
                       article.text,
                       tweet['timestamp'],
                       self.country,
                       self.source, 
                       tweet['text']]
        return out_article

    def tweets_to_articles(self, tweets, limit=1e10):
        """
        param: tweets is a list of dict.
        """
        nb_articles = 0
        scraped_articles = []
        for i, tweet in enumerate(tweets):
            if tweet['username'] == self.source and len(tweet['links'])>0:
                read_articles = list(map(
                    lambda url: self.read_article(tweet, url), tweet['links']))
                scraped_articles.extend(read_articles)
                nb_articles += len(read_articles)
            if nb_articles > limit:
                break

        print(f'Found {nb_articles} articles over the {len(tweets)} tweets')
        return scraped_articles
    

        
    def read_all(self, max_iter=10):
        """
        Get list of lists of articles.
        """
        config = newspaper.Config()
        config.memoize_articles = False
        paper = newspaper.build(self.website, 
                                language=self.language,
                                config=config) 
        articles = []
        iter_ = 0
        print("PAPER", paper.articles)
        for article in tqdm.tqdm(paper.articles):
            print("URL:", article.url)
            row, _ = self.read_article(article.url)
            articles.append(row)
            iter_ += 1
            if iter_ > max_iter:
                break
        return articles, header           

sources_senegal = { "Le Soleil": "http://lesoleil.sn",  
                    "Le Quotidien": "https://www.lequotidien.sn"}

sources_algeria = {}
def scrap_country(country, 
                    language="fr", 
                    max_iter=1000,
                    path='../data/'):
    assert country in sources.keys(), "Error with the country name "
    local_sources = sources[country]
    for name, website in local_sources.items():
        print('Start Scraping the information from {} | {}'.format(name, 
                                                website))
        scraper = ArticleScrapper(country=country,
                                source=name, 
                                website=website, 
                                language=language)
        articles, header = scraper.read_all(max_iter=max_iter)
        filename = "".join(name.lower().split())
        filename = path+filename+'.json'
        save(articles, header, filename)
'''

class ArticleScrapper:
    """
    Class to read find urls from tweets and 
    format the data under the relevant format.
    """
    def __init__(self,
                 country: str,
                 source: str,
                 language="fr"):
        self.country = country
        self.language = language
        self.source = source
        self.counter = 0
        #self.header = header

    def create_id(self, article):
        _id = "{}_{}_{}".format(self.country, self.source, self.counter)
        self.counter += 1
        return _id

    def read_article(self, tweet, url):
        config = newspaper.Config()
        config.memoize_articles = False
        article = Article(url, language=self.language, config=config)
        try:
            article.download()
            article.parse()
            _id = self.create_id(article)
            out_article = [_id,
                           article.title,
                           article.text,
                           tweet['timestamp'],
                           self.country,
                           self.source,
                           tweet['text']]
        except Exception as e:
            print(f'Caught {e}')
            out_article = ['Error',
                            '',
                            '',
                            tweet['timestamp'],
                            self.country,
                            self.source,
                            tweet['text']]
        return out_article

    def tweets_to_articles(self, tweets, limit):
        """
        param: tweets is a list of dict.
        limit: max number of articles to get from th tweets
        """
        nb_articles = 0
        scraped_articles = []
        for tweet in tqdm.tqdm(tweets):
            if tweet['screen_name'] == self.source and len(tweet['links']) > 0:
                read_articles = list(map(
                    lambda url: self.read_article(tweet, url), tweet['links']))
                scraped_articles.extend(read_articles)
                nb_articles += len(read_articles)
            if nb_articles > limit:
                break

        print(f'Found {nb_articles} articles over the {len(tweets)} tweets')
        return scraped_articles


def get_tweets(username, 
                limit,
                bd, 
                ed, 
                root):
    
    #scrap_country(country=args.country)
    output_path = root + "tweets_" + username + "_"+ bd + "_"+ ed +'.json'
    to_run = ["twitterscraper",
              f"{username}",
              f"--limit={limit}",
              f"-bd={bd}",
              f"-ed={ed}",
              f"--output={output_path}"]
    subprocess.call(to_run)
    print(f'Saved tweets in {output_path}')
    return output_path


def scrap_country(country,
                  language,
                  limit,
                  scrap_tweets,
                  bd,
                  ed,
                  root):
    
    assert country in sources.keys(), "Error with the country name"
    local_sources = sources[country]
    for source in local_sources:
        print('Start Scraping the information from {} | {}'.format(country,
                                                                   source))
        if scrap_tweets:
            output_path = get_tweets(source, limit, bd, ed, root)
        else:
            output_path = root + "tweets_" + source + "_" + bd + "_" + ed + '.json'
        
        with open(output_path, 'r') as reader:
            tweets = json.load(reader)
        print(f'Loading {len(tweets)} tweets')

        scraper = ArticleScrapper(country=country,
                                  source=source,
                                  language=language)
        
        articles = scraper.tweets_to_articles(tweets, limit)
        
        out_dic = {'head': header,
                   'articles': articles}

        filename = root + "articles_" + source + "_" + bd + "_" + ed + '.json'
        
        with open(filename, 'w') as writer:
            json.dump(out_dic, writer, indent=4)





#=======================================================
# Test classes, functions
def test_scrap_tweets():
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

def test_article_scrap():
    url = "https://www.senenews.com/actualites/coronavirus-des-proprietaires-refusent-de-louer-leurs-hotels-a-letat-macky-sall-utilise-la-methode-forte_305133.html"
    sene_scraper = ArticleScrapper('Senegal', 'SeneNews') 
    row, header = sene_scraper.read_article(url)
    print('row')

def test_website_scrap():
    #config = newspaper.Config()
    #config.memoize_articles = False
    #help(newspaper.build)
    #paper = newspaper.build('http://lesoleil.sn', language="fr", config=config)
    #print(paper.articles)

    #crap_senegal = ArticleScrapper("Senegal", "Le Soleil",  "http://lesoleil.sn")
    #articles, header = scrap_senegal.read_all(max_iter=2)
    scrap_senegal = ArticleScrapper(
        "Senegal", "Le Quotidien", "https://www.lequotidien.sn")
    articles, header = scrap_senegal.read_all(max_iter=2)
    save(articles=articles, 
        header=header, 
        path="../data/lequotidien.json")
    print('debug')

    #row, header = scrap_senegal.read_article(
    #    "https://www.lequotidien.sn/editorial-macky-sall-sur-les-lecons-a-tirer-de-la-crise-du-coronavirus-dans-le-monde-apprendre-de-nos-erreurs-et-de-nos-limites-et-redefinir-lordre-des-priorites/")
    #print(row)
    #print('debug')
    
        
if __name__ == "__main__":
    #test_scrap_tweets()
    #test_article_scrap()
    #test_website_scrap()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--country', type=str)
    #parser.add_argument('--newspapers', action='store_true', default=True)
    parser.add_argument('--bd', type=str, default="2020-02-01")
    parser.add_argument('--ed', type=str, default="2020-04-12")
    parser.add_argument('--limit', type=int, default=10000000)
    parser.add_argument('--root', type=str, default='../data/', help='Path to the data file')
    parser.add_argument('--language', type=str, default="fr")
    parser.add_argument('--scrap_tweets', action='store_false', default=True)

    args = parser.parse_args()
    print('Running with the following arguments: {}'.format(args))
    scrap_country(args.country,
                  args.language,
                  args.limit,
                  args.scrap_tweets,
                  args.bd,
                  args.ed,
                  args.root)
    

   


