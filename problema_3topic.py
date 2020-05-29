
import pandas as pd
from nltk.tokenize import word_tokenize
import math
import re

df = pd.read_csv('results.csv', delimiter=',')





########################################PRELUCRARE TEXT####################################################

def pre_process(text):
    # lowercase
    text = text.lower()

    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'#+', ' ', text)
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = re.sub(r"([A-Za-z]+)'s", r"\1 is", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"won't", "will not ", text)
    text = re.sub(r"isn't", "is not ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"a href", " ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub('\s+', ' ', text)
    # remove tags
    text = re.sub("<!--?.*?-->", "", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    return text

#am eliminat tot ce mi s a parut mie relevant pentru o precizie mult mai buna
#de asemenea am adaugat o inlocuire a prescurtarilor


docs= df['body'].apply(lambda x: pre_process(x))

def get_document_freq_dict(sents):
    freq_dicts=[]
    for sent_index, sent in enumerate(sents):
        freq_dict = {}
        tokens = word_tokenize(sent)
        tokens = [token.lower() for token in tokens]

        for token in tokens:
            if freq_dict.get(token):
                freq_dict[token] += 1
            else:
                freq_dict[token] = 1

        data_collector = {'sent_id': sent_index, 'sent_length': len(tokens), 'freq_dict': freq_dict}
        freq_dicts.append(data_collector)

    return freq_dicts

# print(get_document_freq_dict(docs))



###################################CALCUL SCOR TF###############################################################

def get_tf(documents_freq_dicts):
    tf_scores = []
    for data_collector in documents_freq_dicts:
        sent_id = data_collector['sent_id']
        for token in data_collector['freq_dict']:
            tf_dict = {
                'sent_id': sent_id,
                'tf_score': data_collector['freq_dict'][token] / data_collector['sent_length'],
                'token': token
            }
            tf_scores.append(tf_dict)
    return tf_scores


# print(get_tf(get_document_freq_dict(docs)))
tff=get_tf(get_document_freq_dict(docs))




##############################CALCUL SCOR IDF###############################################################








def get_idf(documents_freq_dict):
    idf_scores = []

    for data_collector in documents_freq_dict:

        for token in data_collector['freq_dict']:


            token_freq_docs = sum([
                token in data_collector['freq_dict']
                for data_collector in documents_freq_dict
            ])

            idf_dict = {
                'sent_id': data_collector['sent_id'],
                'idf_score': math.log(len(documents_freq_dict) / token_freq_docs),
                'token': token,


            }

            idf_scores.append(idf_dict)

    return idf_scores


# print(get_idf(get_document_freq_dict(docs)))
hh=get_idf(get_document_freq_dict(docs))



#####################################PRELUCRARE SCOR###########################################################


##partea de mai sus cu scorurile tf si idf sunt comentate la curs si am folosit acelasi principiu/cod

# scorul de tf-idf cel mai mare este acela care poate fi subiectul
#ca sa nu mai adaug alt camp am suprapus pest scorul idf scorul de tf-idf
#de asemenea este prima oara cnad afisez ca sa se vada corectitudinea scorurilor tf-idf




i=0



while(i<len(hh)):

    print(hh[i])
    print (tff[i])
    # print( hh[i]['idf_score'])
    hh[i]['idf_score']= hh[i]['idf_score']* tff[i]['tf_score']

    print("Scorul tf-idf:")
    print( hh[i]['idf_score'])
    i=i+1


##################################SELECTIA TOPICURILOR##########################################################


# la procesul de selectie mai hotarat sa lucrez pe soratrea dictionarelor din liste mi s a parut cea mai eficienta varianta
#in principiu am luat scorirule pentru fiecare post in parte si le am pus intr o lista cca dupa aceea sa pot sorta acea lista
#descrescator cu scorul tf-idf pentru a putea obtine pe primele 3 locuri topicurile noastre. nu mergea sa dau direct append
#la data collector asa ca am construit un dictionar paralel.
#astfel outputul nostru va avea o lista de dictionare cu 2 campuri, campul pentru topic are la randul lui un dictionar mi s a
#parut cca relevant sa pun si scorurile.





def selectie(documents_freq_dict):


    i=0
    l=list()
    df3=[]
    for data_collector in documents_freq_dict:
        # print(data_collector)
        if int(data_collector['sent_id'])==i:
            d3={
             'tf_idf_score':data_collector['idf_score'],
             'token':data_collector['token']
            }
            l.append(d3)
        else:
            l=sorted(l, key=lambda y: y['tf_idf_score'],reverse=True)
            #sorteaza dupa valoare lui tf-idf

            dict3 = {
                'post_id': i,
                'topics': l[:3]
                # ia ultimele 3 elemente din lista
            }
            df3.append(dict3)
            l=[]
            i = data_collector['sent_id']
            d3 = {
                'tf_idf_score': data_collector['idf_score'],
                'token': data_collector['token']
            }
            l.append(d3)


    l = sorted(l, key=lambda y: y['tf_idf_score'], reverse=True)
    dict3 = {
        'post_id': i,
        'topics': l[:3]
    }
    df3.append(dict3)
    # in df avem o lista cu cele 3 topicuri
    print(df3)


selectie(hh)
