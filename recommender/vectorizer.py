from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from typing import Tuple

def tf_idf(df: pd.DataFrame, content_col: str = 'processedContent') -> Tuple[TfidfVectorizer, pd.DataFrame]:
    tfidf = TfidfVectorizer(use_idf=True, smooth_idf=False)
    tfidf_matrix = tfidf.fit_transform(df[content_col])

    df_tfidf = pd.DataFrame(
        tfidf_matrix.toarray(),
        index=df['title'],
        columns=tfidf.get_feature_names_out()
    )

    return tfidf, df_tfidf
