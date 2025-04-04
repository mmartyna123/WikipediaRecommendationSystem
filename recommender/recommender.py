import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
from recommender.vectorizer import tf_idf
from typing import List
from recommender.expansion import expandDatabase



def recommendArticles(history: List[str], df: pd.DataFrame, tokenizer, stemmer=None, lemmatizer=None, useLemmatizer: bool = False,
    top_n: int = 5, explanation_terms: int = None) -> pd.DataFrame:
    
    
    if df.index.name != 'title':
        df = df.set_index('title')

    # ✅ Expand database and filter valid history titles
    df, matched_history = expandDatabase(history, df, tokenizer, stemmer, lemmatizer, useLemmatizer)

    if not matched_history:
        raise ValueError("None of the entered titles were found or could be fetched.")

    tfidf, dfTFIDF = tf_idf(df.reset_index())
    history_content = ' '.join(df.loc[matched_history, 'processedContent'])
    history_vector = tfidf.transform([history_content]).toarray()[0]

    cosine_distances = dfTFIDF.apply(lambda row: cosine(row, history_vector), axis=1)
    similarity_scores = 1 - cosine_distances

    recommendations = pd.DataFrame({
        'title': dfTFIDF.index,
        'link': df['link'],
        'similarity': similarity_scores
    })

    recommendations = recommendations[~recommendations['title'].isin(matched_history)]
    recommendations = recommendations.sort_values(by='similarity', ascending=False).reset_index(drop=True)
    recommendations = recommendations.head(top_n)
    
    feature_names = tfidf.get_feature_names_out()
    if explanation_terms == 0:
        recommendations['explanation'] = ["(no explanation)"] * len(recommendations)
    else:
        explanations = []
        for _, row in recommendations.iterrows():
            vector = dfTFIDF.loc[row['title']].values
            top_indices = np.argsort(vector)[-explanation_terms:][::-1]
            terms = [feature_names[i] for i in top_indices]
            explanations.append(", ".join(terms))
        recommendations['explanation'] = explanations



    return recommendations.head(top_n)
