from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import collections
import pymongo


client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client['scrapping']
collection=db['discription']
data1=collection.find({})
ps = PorterStemmer()
c=1
for i in data1:
    s=[]
    print(c)
    for j in range(len(i['para'])):
        s.append(ps.stem(i['para'][j]))
    collection.update_one({"para":i['para']},{"$set":{"para": s }})
    c+=1