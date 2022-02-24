import re
from netrc import netrc
import pandas as pd
import unicodedata
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
# from mysql.connector import connection, cursor
# import mysql.connector

cached_stopwords = stopwords.words('english')


# def make_mysql_connection():
#     global connection, cursor
#     connection = mysql.connector.connect(host='127.0.0.1', database='libertyitems', user='kenfore',
#                                          port='3306', password='fDSCYldCuWpjuXUe')
#     cursor = connection.cursor()
#     cursor.execute("SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
#
#
# def get_df_from_mysql_query(sql_text):
#     global connection, cursor
#     if not connection.is_connected():
#         make_mysql_connection()
#
#     df = pd.read_sql(sql_text, con=connection)
#     return df


def get_panda_val(panda_var):
    if pd.isna(panda_var.tolist()):
        return 'Unknown'
    else:
        return str(panda_var.tolist()[0]).strip().strip('-')


def get_item_detail(item_df, prod_id,identifier,attribute_1,attribute_2):
    try:
        row = item_df.loc[item_df[identifier] == prod_id]
        text_val = clean_item_title(get_panda_val(row[attribute_1])) + ' - in ' + get_panda_val(row[attribute_2]) + ' (ID:' + str(prod_id) + ')'
        return text_val
    except:
        return str(prod_id) + ' - item Name Not Found'


def get_item_title(item_df, prod_id,identifier,attribute_1):
    try:
        prod_id = int(prod_id)
        row = item_df.loc[item_df[identifier] == prod_id]
        return str(clean_item_title(get_panda_val(row[attribute_1])))
    except:
        return str(prod_id) + ' - item Name Not Found'


def clean_item_title(text):
    new_text = str(text)
    # new_text = new_text.replace('-', '').replace(':', '').replace(';', '').replace('.', '').strip()
    new_text = re.sub('[^0-9a-zA-Z ]+', '', new_text)
    return new_text.strip()


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


# def replace_numbers(words):
#     """Replace all interger occurrences in list of tokenized words with textual representation"""
#     p = inflect.engine()
#     new_words = []
#     for word in words:
#         if word.isdigit():
#             new_word = p.number_to_words(word)
#             new_words.append(new_word)
#         else:
#             new_words.append(word)
#     return ''.join([str(letter) for letter in new_words])


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


def normalize(words):
    words = remove_nonlatin(words)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = lemmatize_verbs(words)
    words = remove_stopwords(words)
    return words  # ''.join([str(letter) for letter in words])
    # return ' '.join([str(word) for word in words])
