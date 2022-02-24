import nltk, string
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from Feature_Processing import Feature_Processing
import numpy as np
import pickle


nltk.download('wordnet')
nltk.download('stopwords')
cached_stopwords = stopwords.words('english')
cached_stopwords.append('amp')

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def init_config():
    global feature_1, feature_2, file_1, file_2, output_file, identifier_1, identifier_2
    api_config = json.load(open("Generate_Data_Config.json"))

    feature_1 = api_config['feature_1']
    feature_2 = api_config['feature_2']

    file_1 = api_config['file_1']
    file_2 = api_config['file_2']

    identifier_1 = api_config['identifier_1']
    identifier_2 = api_config['identifier_2']

    output_file = api_config['output_result']


def stem_tokens(tokens):
    value=[stemmer.stem(item) for item in tokens]
    return value

'''remove punctuation, lowercase, stem'''
def normalize(text):
    value=stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
    return value

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


feature_1=feature_2=file_1=file_2=output_file=identifier_1=identifier_2=''
init_config()

df_one=Feature_Processing(file_1,feature_1)
df_two=Feature_Processing(file_2,feature_2)

out_put={}

print(df_one.head())
print(df_two.head())

for index,row in df_one.iterrows():
    out_put[row[identifier_1]]=[(row_two[identifier_2], np.float16(cosine_sim(row['feature_combination'],row_two['feature_combination']))) for i,row_two in df_two.iterrows()]

# # values={55: [(1, 3.22), (2, 2.22), (3, 1.22)], 214: [(1, 3.22), (3, 2.22), (2, 1.22)]}
#
# dic={}
# id_1=[]
# id_2=[]
# sim=[]
# for value in out_put.keys():
#     temp=(0,1)
#     for item in out_put[value]:
#         id_1.append(value)
#         id_2.append(item[0])
#         sim.append(item[1])
#         # print(str(value)+" : "+str(temp[0])+" : "+str(temp[1]))
# print(str(id_1)+" : "+str(id_2)+" : "+str(sim))
# import numpy as np
# id_new_2=np.unique(np.array(id_2)).tolist()
# dic=dic.fromkeys(id_new_2)
# for key in dic.keys():
#     dic[key]=[]
# for idx,i in enumerate(id_2):
#     dic[i].append((id_1[idx],sim[idx]))
# print(out_put)
# print(dic)

for value in out_put:
    out_put[value].sort( key = lambda x: -x[1])
print(out_put)

# for value in dic:
#     dic[value].sort( key = lambda x: -x[1])
# dic={k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse=True)}
# print(dic)


with open(output_file, 'wb') as f:
    pickle.dump(out_put, f)

# with open("dic"+output_file, 'wb') as f:
#     pickle.dump(dic, f)
