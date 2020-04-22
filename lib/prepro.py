import seaborn as sns
import datetime
from collections import Counter
import spacy
import fr_core_news_md
import tqdm

import json
import pandas as pd
import os
try:
    spacy.load('fr_core_news_md')
except Exception as e:
    print(e)



def clean_index_text(df):
    """
    Clean up the id part and replace empty 
    articles by tweets.
    """
    id_name = "{}_{}_".format(df.iloc[0].country, df.iloc[0].source)
    id_ = [id_name + str(i) for i in range(len(df))]
    df['id'] = id_
    for i in range(len(df)):
        if df.iloc[i].text == '':
            print(f'Empty text for {i}, use tweet instead')
            df.loc[i, 'text'] = df.iloc[i]['tweet']
    return df


def clean_text(text_, nlp):
    """
    Function to remove line break, double spaces...
    """
    text_ = text_.rstrip()
    text_ = text_.replace(u'\xa0', u'')  # Latin normalization
    text_ = text_.replace('\n', ' ')
    text_ = text_.replace('#', '')
    text_ = text_.replace("  ", " ")

    text_ = text_.replace('[^\w\s]', '')
    #lower_ = lambda x: " ".join(x.lower() for x in x.split())
    #text = lower_(text)
    doc = nlp(text_)
    return doc


def get_stats(index, clean_df, nlp, key_words):
    """
    Function to count the key words found in the text with time. 
    Add a new column to the dataframe.
    """
    df = clean_df
    count = Counter()
    Text = df.iloc[index].text
    Title = df.iloc[index].title
    date = df.iloc[index].Date
    doc = clean_text(Title + Text, nlp)

    low_key_words = map(lambda x: x.lower(), key_words)
    key_words.extend(list(low_key_words))
    print(Title, df.iloc[index].Date)
    count = Counter()
    count_key = Counter()
    for token in tqdm.tqdm(doc):
        if token.pos_ in ['PROPN', 'NOUN', 'VERB', 'ADJ']:
            #print(token.text, token.pos_, token.dep_)
            count.update([token.text.lower()])
        if token.text in key_words:
            count_key.update([token.text.lower()])
    return Title, count_key, date


def clean_date(date_str):
    """
    Modify the date into a timestamp format
    """
    dmy, hms = date_str.split('T')
    dmy = "/".join(dmy.split('-')[::-1])
    element = datetime.datetime.strptime(dmy,
                                         "%d/%m/%Y")
    return element


def visualize(index, clean_df):
    """
    Functioo to get histograms 
    the key words we're interested in
    and the main topics more generally speaking.
    """
    df = clean_df
    count = Counter()
    Text = df.iloc[index].text
    Title = df.iloc[index].title
    doc = clean_text(Title+Text)
    key_words = ['Corona', 'Covid19',
                 'Covid', 'Covid-19',
                 'Virus', 'Pandémie',
                 'Maladie', 'Coronavirus',
                 'Santé']
    low_key_words = map(lambda x: x.lower(), key_words)
    key_words.extend(list(low_key_words))
    #print(Text)
    print(Title, df.iloc[index].Date)
    count = Counter()
    count_key = Counter()
    for token in doc:
        if token.pos_ in ['PROPN', 'NOUN', 'VERB', 'ADJ']:
            #print(token.text, token.pos_, token.dep_)
            count.update([token.text.lower()])
        if token.text in key_words:
            count_key.update([token.text.lower()])
    print(count_key)

    labels, values = zip(*count.most_common()[:10])
    fig = go.Figure(data=[go.Histogram(x=labels, y=values, histfunc='sum')])
    fig.show()
    try:
        labels_key, values_key = zip(*count_key.most_common()[:10])
        fig = go.Figure(
            data=[go.Histogram(x=labels_key, y=values_key, histfunc='sum')])
        fig.show()
    except:
        print('No "key word" in this doc')


header = ['id',
          'title',
          'text',
          'Date',
          'country',
          'source',
          'tweet']

key_words = ['Corona', 'Covid19', 'Covid', 'Covid-19',
             'Virus', 'Pandémie', 'Maladie', 'Coronavirus']


def main(read_path):   
    with open(read_path, 'r') as reader:
        data = json.load(reader)
    df = pd.DataFrame(columns=header,
                    data=data['articles'])
    
    #Drop duplicates, NAN
    print('Start cleaning the dataframe')
    clean_df = df.drop('id', axis=1).drop_duplicates(keep='first')
    clean_df = clean_df[~clean_df['Date'].isna()]

    nlp = fr_core_news_md.load()

    clean_df = clean_index_text(clean_df)
    clean_df = clean_df[~clean_df['Date'].isna()]

    low_key_words = map(lambda x: x.lower(), key_words)
    key_words.extend(list(low_key_words))


    #Clean date and reset index
    clean_df = clean_df.sort_values('Date')
    clean_df.reset_index(drop=True, inplace=True)
    #Get indices, freq
    freq_ = []
    for index in tqdm.trange(len(clean_df), desc='Looping through the artices'):
        _, counter, date = get_stats(index, clean_df, nlp, key_words)
        freq_.append(sum(counter.values()))

    clean_df['freq'] = freq_
    return clean_df

if __name__ == "__main__":
    pass
    #example_article = 'articles_JourDuMali_2020-02-01_2020-04-14.json'
    #example_path = os.path.join('../data', example_article)
    #clean_df = main(example_path)

