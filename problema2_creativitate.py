import pandas as pd

from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt




df = pd.read_csv('results.csv', delimiter=',')
tags= df['tags'].values




print(tags)
l=""
for i in tags:
    print(i)
    l=l+"|"+str(i)


#stergem unde avem nan si separam prin | ca asa este specificat in csv
l=l.replace("|nan","")
l=l.replace("|"," ")
l=l.replace("-","")
# print(len(l))







pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
text = pattern.sub('', l)
#in cazul noastru nu sunt stop words se poate observa din len dar ar fi bine sa verificam totusi acest aspect
# print(len(text))
list=[text]





# create the transform
vectorizer = CountVectorizer()

# tokenize and build vocab
vectorizer.fit(list)
# summarize
print(vectorizer.vocabulary_)
dict=vectorizer.vocabulary_





tags=[]
apps=[]
for tag,app in dict.items():
    tags.append(tag)
    apps.append(app)

a = sorted(dict.items(), key=lambda x: x[1],reverse=True)
# print(a)


# plt.bar(tags,apps, label="Primul Bar Grafic")
# plt.legend()
# plt.xlabel('tags')
# plt.ylabel('aparitii')
# plt.title('tagurile in functie de nr de utilizatori ai acestora')
# # plt.show()

#TREBUIE SA TRANSFORMAM IN LISTA CA SA PUTEM FACE GRAFICELE

# tags=[]
# apps=[]
# for tag,app in a:
#         tags.append(tag)
#         apps.append(app)
#
# plt.bar(tags[:10],apps[:10], label="Grafic cele mai populare 10 taguri")
# plt.bar(tags[-10:],apps[-10:], label="Grafic cele mai nepopulare 10 taguri")
# plt.legend()
# plt.xlabel('tags')
# plt.ylabel('aparitii')
# plt.title('tagurile in functie de nr aparitiile acestora ai acestora')
# plt.show()
#




#vrem sa aflam care s top cele mai vizionate postari
titles=df['title'].values
bodys=df['body'].values
views= df['view_count'].values
print(views[0])
print(bodys[0])
vizualizari=[]
for i in range(len(bodys)):
    d1={
        #aici poate avea o multime de campuri dar eu le am ales pe acestea ca sa mi fie mai usor sa verific
        # 'body':bodys[i],
        'view_count':views[i],
        'title': titles[i]
    }
    vizualizari.append(d1)

print(vizualizari)
# using sorted and lambda to print list sorted

print("Lista sortata dupa vizualizari : ")
print(sorted(vizualizari, key = lambda i: i['view_count'],reverse=True))
print('Top 5 postari cu cele mai multe vizualizari:')
vizualizari=sorted(vizualizari, key = lambda i: i['view_count'],reverse=True)
print(vizualizari[:5])



# FACEM DIN NOU LISTE PENTRU A FACE NISTE GRAFICE
titles2=[]
views2=[]
for i in range(len(vizualizari)):
            titles2.append(vizualizari[i]['title'])
            views2.append(vizualizari[i]['view_count'])

plt.bar(titles2[:5],views2[:5], label="intrebarile cu cele mai multe vizualizari")
plt.legend()
plt.xlabel('titles')
plt.ylabel('vizualizari')
plt.title('intrebarile cu cele mai multe vizualizari')
plt.show()
