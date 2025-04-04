import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict


def crawlArticles(start_url, max_articles):
    visited = set() # set of visited pages to keep the ones that have already been crawled
    to_visit = [start_url] # a list of pages yet to be crawled, starting with the start_url
    articles = [] # a list to store the details of the articles (title, link and content)
    
    # a loop to check if there are pages to visit and if the number of articles is less than the max_articles
    while to_visit and len(articles) < max_articles:
        page = to_visit.pop(0) # get the first page in the list
        if page in visited:
            continue
        visited.add(page) # add the page to the visited set
        
        try:
            response = requests.get(page) # geting the page
            response.raise_for_status() 
            soup = BeautifulSoup(response.content, 'html.parser') # parsing the page
            
            # extracting the title and content of the article
            title = soup.find('h1').text # article's title
            paragraphs = soup.find_all('p') # article's paragraphs
            content = ' '.join([p.text for p in paragraphs]) # article's content that is inside paragraphs
            articles.append({"title": title, "link": page, "content": content})
            
            # extracting and filtering new links
            for link in soup.find_all('a', href=True): # we look for all links in the page
                href = link['href']
                # we ensure that no page that has parts like 'disambiguation' or is a 'Main_Page' would be visited and added to the database
                if href.startswith('/wiki/') and ':' not in href and '#' not in href and 'Main_Page' not in href and 'disambiguation' not in href:
                    full_url = "https://en.wikipedia.org" + href
                    if full_url not in visited:
                        to_visit.append(full_url) # adding the new link to the list of pages to visit
                        
            time.sleep(0.5) # need to be polite to Wikipedia
            
        except:
            pass
        
    return articles
