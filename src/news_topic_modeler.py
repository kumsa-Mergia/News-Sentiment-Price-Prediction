import pandas as pd
import re
import string
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import traceback


class AnalystHeadlineTopicModeler:
    def __init__(self, filepath, target_stocks, n_topics=5):
        self.filepath = filepath
        self.target_stocks = target_stocks
        self.n_topics = n_topics
        self.df = None
        self.df_filtered = None
        self.vectorizer = CountVectorizer(stop_words='english', max_df=0.95, min_df=2)
        self.lda_model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        self.feature_names = None
        self.topic_keywords = {}

    def load_and_filter_data(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        self.df = pd.read_csv(self.filepath)

        if 'stock' not in self.df.columns:
            raise ValueError("Missing 'stock' column in data")

        self.df_filtered = self.df[self.df['stock'].isin(self.target_stocks)].copy()

        if self.df_filtered.empty:
            raise ValueError("No rows matched the target stock list.")

    def clean_text(self, text):
        try:
            text = text.lower()
            text = re.sub(r"http\S+", "", text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = re.sub(r'\d+', '', text)
            return text
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return ""

    def preprocess_headlines(self):
        if 'headline' not in self.df_filtered.columns:
            raise ValueError("Missing 'headline' column in data")

        self.df_filtered['clean_headline'] = self.df_filtered['headline'].astype(str).apply(self.clean_text)

    def vectorize_text(self):
        try:
            X = self.vectorizer.fit_transform(self.df_filtered['clean_headline'])
            if X.shape[0] == 0:
                raise ValueError("Vectorized matrix is empty — check input data or filtering conditions.")
            self.feature_names = self.vectorizer.get_feature_names_out()
            return X
        except Exception as e:
            raise RuntimeError(f"Error during vectorization: {e}")

    def fit_lda_model(self, X):
        try:
            self.lda_model.fit(X)
        except Exception as e:
            raise RuntimeError(f"Error fitting LDA model: {e}")

    def extract_topics(self, no_top_words=10):
        try:
            for topic_idx, topic in enumerate(self.lda_model.components_):
                keywords = [self.feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
                self.topic_keywords[f"Topic {topic_idx+1}"] = keywords
        except Exception as e:
            raise RuntimeError(f"Error extracting topics: {e}")

    def display_topics(self):
        if not self.topic_keywords:
            print("No topics to display.")
        else:
            for topic, words in self.topic_keywords.items():
                print(f"\n{topic}: {', '.join(words)}")
                
    def run(self):
        try:
            print("Loading and filtering data...")
            self.load_and_filter_data()
            print(f"Filtered rows: {len(self.df_filtered)}")
            print("Preprocessing headlines...")
            self.preprocess_headlines()
            print("Vectorizing text...")
            X = self.vectorize_text()
            print("Fitting LDA model...")
            self.fit_lda_model(X)
            print("Extracting topics...")
            self.extract_topics()
            print("Displaying topics...")
            self.display_topics()
            return X  # return document-term matrix for visualization
            
        except Exception as e:
            print(f"\n Error: {e}")
            traceback.print_exc()  # Show full traceback
            return None
