# Covid Risk Analysis :earth_af:
## Development branch :hammer:

Project that consists in leveraging different sources of information to better inform, track and prepare the covid crisis in some specific countries
## Structure of our repository
  - lib: Our library and code base
  
  - notebooks: Results, data analysis
  
  - misc: Miscellaneous documents and files
## How to use
- You can put the twitter usernames that interest you in the sources.py file (see example of sources_senegal) and then complete the sources dict.


- To run, do the following ```python scrapers.py --country=Senegal --bd=2020-01-01 --ed=2020-04-14 ```
- It will download the tweets in a file (see data folder), and then read the tweets, get the links, and make articles out of those urls.
- Eventually, all of it is saved in a json file in the data folder. The file is simply a dictionnary with keys "header" and "articles".
- If you succesfully downloaded the tweets, but you had a problem with the articles and you dont want to download the tweets one more time, add ```--scrap_tweets``` to the command line arguments. 
 
## Supported countries
For now, our approach focuses on French speaking countries on the African continent.
Our data includes the following countries:
- Senegal :senegal:
