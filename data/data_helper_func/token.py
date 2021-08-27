import collections
import pymongo
from pymongo.operations import InsertOne
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User,auth
from rest_framework.authtoken.models import Token
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def remove_stopwords():
    
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['scrapping']
    collection=db['discription']
    data1=collection.find({})
    for i in data1:
        words = list(stopwords.words('english'))
        add_list=['.',',',';',':',"/",')','(','[',']','{','}','-','#','"',"'",'’','?','@','!',"''",'``','``','“','”']
        words=words+add_list
        try:
            word_tokens = word_tokenize(i['para'])
        except:
            word_tokens = word_tokenize(" ".join(i['para']))
        else:
            s=[]
            for j in word_tokens:
                if j.lower() not in words:
                    s.append(j)
        s=[]
        for j in word_tokens:
            if j not in words:
                s.append(j)
        collection.update_one({"para":i['para']},{"$set":{"para": s }})


def steming_data(request):
    
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['scrapping']
    collection=db['discription']
    data1=collection.find({})
    ps = PorterStemmer()
    for i in data1:
        s=[]
        for j in range(len(i['para'])):
            s.append(ps.stem(i['para'][j]))
        collection.update_one({"para":i['para']},{"$set":{"para": s }})
