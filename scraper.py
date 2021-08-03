#scraper.py
import pandas as pd
from xml.dom import minidom
import re
from collections import Counter
import itertools


#input: reddit RSS feed in XML format
#output: dataframe (post title,link,time stamp) with each row representing a reddit post
def reddit_extract(file):
    mydoc = minidom.parse(file)
    titles = mydoc.getElementsByTagName('title')
    links = mydoc.getElementsByTagName('link')
    updates = mydoc.getElementsByTagName('updated')

    titles_df = [(elem.firstChild.data) for elem in titles]
    links_df = [(elem.attributes['href'].value) for elem in links]
    updates_df = [(elem.firstChild.data) for elem in updates]
    #deleting the header elements
    del titles_df[0]
    del links_df[:2]
    del updates_df[0]
    df = pd.DataFrame(
        {'title': titles_df,
         'link': links_df,
         'update': updates_df
         })
    return df


#input: post title in string format
#output: list of ticker symbols with $xyz notation (e.g. $AAPL)
def ticker_extract(title):
    tickers = re.findall('\$[a-zA-Z]+', title)
    return tickers


#input: reddit RSS feed in XML format
#output: dictionary mapping the frequency of ticker symbols
def count_ticker(file):
    df = reddit_extract(file)
    titles_list = df['title']
    tickers = []
    for title in titles_list:
        t = ticker_extract(title)
        tickers.append(t)
    merged = list(itertools.chain.from_iterable(tickers))

    #dict = {}
    #for x in merged:
        #if x in dict:
         #   dict[x] += 1
        #if x not in dict:
         #   dict[x] = 1
    #print(dict)

    frequency_res = Counter(merged)
    print(frequency_res)
    return frequency_res


if __name__ == '__main__':
    count_ticker('reddit.xml')