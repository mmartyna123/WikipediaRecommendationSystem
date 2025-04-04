import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from recommender.crawler import crawlArticles
from recommender.preprocessing import preprocessArticles, get_stemmer, get_lemmatizer


def fetchUnknownArticle(unknowTitle, tokenizer, stemmer=None, lemmatizer=None, useLemmatizer=False):
    base_url = "https://en.wikipedia.org/wiki/"
    url = base_url + unknowTitle.strip().replace(' ', '_')

    try:
        print(f"Fetching from: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs if p.text])

        processedArticle = preprocessArticles(content, tokenizer, stemmer, lemmatizer, useLemmatizer)

        return {
            "title": unknowTitle,
            "link": url,
            "content": content,
            "processedContent": processedArticle
        }

    except Exception as e:
        print(f"Failed to fetch article '{unknowTitle}' from {url}: {e}")
        return None

        
        
        
def additionalArticles(newArticle, df, tokenizer, stemmer=None, lemmatizer=None, useLemmatizer=False, maxExpansion=50):
    mainArticle = fetchUnknownArticle(newArticle, tokenizer, stemmer, lemmatizer, useLemmatizer) #fetching the main article taht is missing in the database but is in user's history
    if mainArticle is None: 
        return []
    
    # expansionNumber = random.randint(5, maxExpansion)
    
    newCrawledArticles = crawlArticles(mainArticle['link'], max_articles=maxExpansion)
    
    processedNewArticles=[]
    for article in newCrawledArticles:
        if article['title'] not in df.index:
            # row = pd.Series({"content": article['content']})
            
            article['processedContent'] = preprocessArticles(article['content'], tokenizer, stemmer, 
                                                          lemmatizer, useLemmatizer)
            processedNewArticles.append(article)
            
    return processedNewArticles




def expandDatabase(history, df, tokenizer, stemmer=None, lemmatizer=None, useLemmatizer=False):
    unknownTitles = [title for title in history if title not in df.index]
    allNewArticles = []

    for title in unknownTitles:
        articleData = fetchUnknownArticle(title, tokenizer, stemmer, lemmatizer, useLemmatizer)
        if articleData:
            allNewArticles.append(articleData)
            crawledArticles = additionalArticles(title, df, tokenizer, stemmer, lemmatizer, useLemmatizer)
            allNewArticles.extend(crawledArticles)

    if allNewArticles:
        additionaldf = pd.DataFrame(allNewArticles).set_index('title')
        additionaldf = additionaldf[~additionaldf.index.duplicated(keep='first')]
        df = pd.concat([df, additionaldf])
        df = df[~df.duplicated(subset='link', keep='first')]
    else:
        print("No new articles found.")
        
    print(f"Number of articles in the database after expansion: {len(df)}")
    
    # Filter available titles based on the original history
    available_titles = [title for title in history if title in df.index]
    return df, available_titles

        