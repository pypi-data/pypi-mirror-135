import pandas as pd
from takeusecases.ml.preprocessing.text_vectorizer import TextVectorizer
from gensim.models import KeyedVectors

class Vectorizer:
    
    def __init__(self, embedding_path):
        """
        Constructor
        
        Parameters
        ----------
        None
    
    	Returns
    	-------
    	Preprocessing
    	"""
        self.word2vec = KeyedVectors.load(embedding_path) 
        self.endoder_cols = {'embedding_mean': ['Message']}
        self.encoder = TextVectorizer(self.endoder_cols , word2vec=self.word2vec)
        

    
    def process(self, df: pd.DataFrame, step_train=True, cols_ignore=None):
        """
        Performs treatments on the data. This includes normalization, 
        feature creation, dimensionality reduction, etc.
        
        Parameters
        ----------            
        df          :  pd.Dataframe
                       Dataframe to be processed
        step_train  :  bool
                       reports whether data will be processed as a training or test
       cols_ignore  :  list
                       columns that identify the row and will be ignored in some
                       preprocessing steps, for example, in standardization

        Returns
    	-------
        pd.Dataframe
        """
        if step_train:
            self.encoder.fit(df)
            df = self.encoder.transform(df)
        else:
            df = self.encoder.transform(df)
        return df
