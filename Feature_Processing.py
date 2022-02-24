# Import the libraries
import pickle
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from termcolor import colored
import unicodedata
import re
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import numpy as np

#
nltk.download('wordnet')
nltk.download('stopwords')
cached_stopwords = stopwords.words('english')
cached_stopwords.append('amp')

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words.split(' '):
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return ' '.join([str(letter) for letter in new_words])


def remove_nonlatin(words):
    words = ''.join([i if 48 <= ord(i) <= 122 else ' ' for i in words])
    try:
        words = (ch for ch in words if unicodedata.name(ch).startswith(('LATIN', 'DIGIT', 'SPACE')))
    except:
        print('Error in: ', words)
        return words

    return ''.join(words)


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words.split(' '):
        new_word = word.lower()
        new_words.append(new_word)
    return ' '.join([str(letter) for letter in new_words])


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words.split(' '):
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return ' '.join([str(letter) for letter in new_words])


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words.split(' '):
        if word not in cached_stopwords:
            new_words.append(word)
    return ' '.join([str(letter) for letter in new_words])


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words.split(' '):
        stem = stemmer.stem(word)
        stems.append(stem)
    return ' '.join([str(letter) for letter in stems])


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words.split(' '):
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return ' '.join([str(letter) for letter in lemmas])


def remove_tags(words):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub(' ', words)


def normalize(words):
    words = remove_tags(words)
    words = remove_nonlatin(words)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = lemmatize_verbs(words)
    words = remove_stopwords(words)
    return words  # ''.join([str(letter) for letter in words])
    # return ' '.join([str(word) for word in words])


def get_important_features(data, features):
    important_features = []
    for i in range(0, data.shape[0]):
        try:

            feature_string=''
            for feature in features:
                feature_string += normalize(str(data[feature][i])) + ' '

            # review_cleaned = normalize(str(data['GoodReadsRev'][i]))
            # feature_string = ( normalize(str(data['Title'][i])) + ' ' + normalize(str(data['Author'][i])) + ' ' + normalize(str(
            #         data['Categories'][i])) + ' ' )
            # feature_string = feature_string * 2
            # feature_string = feature_string + str(review_cleaned)
                    # repeat title, author and categories twice to give them more impact
            important_features.append(feature_string)
            if i < 100:
              print(feature_string)
        except:
           print('Invalid data ',(i, str(data[i])))
           for feature in features:
               feature_string += normalize(str(data[feature][i])) + ' '
           important_features.append(feature_string)

    return important_features


def data_processing(df,features):
    df.drop_duplicates(inplace=True, keep="last")

    for feature in features:
        df[df[feature].str.strip().astype(bool)]
        df[feature].replace('', np.nan, inplace=True)
        df[feature].replace(' ', np.nan, inplace=True)

        # df.dropna(axis=0, subset=features, thresh=2, inplace=True)

    # print("DF before prining", len(df))

    # df.dropna(axis=0, subset=['Title', 'Author', 'GoodReadsRev'], thresh=2, inplace=True)
    # df.dropna(axis=0, subset=['GoodReadsRev'], inplace=True)
    # df.reset_index(inplace=True)

    # remove all rows where GoodReadsRev is just the combination of Title and Author
    # df = df[~(df.GoodReadsRev.str.len() <= (df.Title.str.len() + df.Author.str.len() + 20))]
    # df.reset_index(inplace=True)

    if df.empty:
        print("No more data in CSV to process... Exiting...")
        exit(0)

    return df

def Feature_Processing(file,features):
    try:
        df = pd.read_csv(file)
        df=data_processing(df,features)

        important_feature_values = get_important_features(df,features)
        df['feature_combination']=important_feature_values

        return df
    except Exception as e:
        print('---------------------------\n-----------------------\n----------------\n',e)
        return df

