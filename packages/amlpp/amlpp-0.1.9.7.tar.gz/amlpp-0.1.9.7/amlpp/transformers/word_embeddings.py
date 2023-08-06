from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from gensim.models import Word2Vec
from nltk.corpus import stopwords

from typing import List

import pandas as pd
import numpy as np
import pymorphy2
import nltk

from ._base_transform import BaseTransform

nltk.download('stopwords')
nltk.download('punkt')

snowball = SnowballStemmer(language="russian")
stop_words = stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer()
##############################################################################
class Word2Vectorization(BaseTransform):
    """Class for transforming text data into numerical vectors
    inserted values based on the rest of the data available
    Parameters
    ----------
    columns: List [str] or None = None
        Column names whose values will be vectorized
    level_formatting: int = 1
        Formatting level
    params: dict = {}
        Parameters for fillers
    """
    def __init__(self, columns:List[str], level_formatting:int = 1, **params):
        self.level_formatting = level_formatting
        self.word2 = {column:None for column in columns}
        self.params = {'epochs':5000, 'min_count':1, 'window':5, 'vector_size':20, **params}
        super().__init__({'columns':columns, 'level_formatting':level_formatting, **self.params})

    def fit(self, X:pd.DataFrame, Y:pd.DataFrame or pd.Series):
        self.word2 = {column:None for column in self.word2}
        for column in self.word2: 
            dictionary = [self.refactor_string(str(i)) for i in X[column]]
            self.word2[column] = Word2Vec(dictionary, **self.params, seed = 42)
        return self

    def transform(self, X:pd.DataFrame, Y:pd.DataFrame or pd.Series = None):
        for column in self.word2:
            X[column] = list([self.mean_word2vec(val, column) for val in X[column]])
        return X

    def refactor_string(self, string:str)->List[str]:
        """ Function for refactoring a string, bringing it back to normal
        Tokenization, getting rid of signs, etc.
        Parameters
        ----------
        string: str
            the string to be refactored
        Returns
        ----------
        refactoring string: List [str] 
            From refactoring a string and converting to an array of strings 
        """
        string = string if str(string) != 'nan' else ""                          # Проверка на NAN
        string = word_tokenize(str(string).lower())                              # Нижний регистр и токенизация
        if self.level_formatting > 0:
            string = [i for i in string if i.isalpha()]                              # Избавления от знаков пунктуации
            if self.level_formatting > 1:
                string = [i for i in string if not i in stop_words]                      # Избавления от стоп слов
                if self.level_formatting > 2:
                    string = [snowball.stem(morph.parse(i)[0].normal_form) for i in string]  # СТЭММИНГ и ЛЕММАТИЗАЦИЯ
        return string

    def mean_word2vec(self, sentence:str, column:str) ->List[float]:
        """ Function of vectorization of proposals
        Parameters
        ----------
        sentence: str
            the sentence to be refactored
        column: str
            The name of the column to which the value belongs
        Returns
        ----------
        vector sentence: List [str]
            Vector clause representations
        """
        vector = self.refactor_string(sentence)
        vector = [self.word2[column].wv[token] for token in vector if token in self.word2[column].wv.key_to_index.keys()]
        return np.mean(vector) if vector != [] else np.nan