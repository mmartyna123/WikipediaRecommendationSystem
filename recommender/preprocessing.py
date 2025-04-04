import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer


stopWords = set(stopwords.words('english'))

def get_stemmer(name: str):
    if name == 'porter':
        return PorterStemmer()
    elif name == 'lancaster':
        return LancasterStemmer()
    else:
        return None
    
    
def get_lemmatizer(name: str):
    return WordNetLemmatizer() 

def preprocessArticles(content: str, tokenizer=word_tokenize, stemmer=None, lemmatizer=None, useLemmatizer=False) -> str:
    tokens = tokenizer(content.lower()) #tokenize and lowercase the text of the articles
    terms = [word for word in tokens if word.isalpha() and word not in stopWords] #removing stopwords and non-alphabetic words
    
    #when the stemmer is not None, we stem the words
    if stemmer:
        processed = [stemmer.stem(word) for word in terms]
    #when the lemmatizer is not None and we want to use it, we lemmatize the words
    elif useLemmatizer and lemmatizer:
        processed = [lemmatizer.lemmatize(word) for word in terms]
    #otherwise, we just return the terms, that were just tokenized, lowercased and the stopweords were removed as well as non-alphabetic words
    else:
        processed = terms
    return ' '.join(processed)
    