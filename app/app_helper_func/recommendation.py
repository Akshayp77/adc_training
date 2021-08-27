import json
from app.serializer import RecomendSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from app.models import Recommend, create_auth_token
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
import pymongo
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from django.http import JsonResponse


def rec(url,user_id,user):

    
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    
    db=client['scrapping']
    collection=db['discription']
    data1=collection.find({})
    l=[]
    for i in data1:
        l.append(" ".join(i['para']))
    vectorize = TfidfVectorizer()
    response = vectorize.fit_transform(l)
    sig=sigmoid_kernel(response,response)
    db=client['scrapping']
    collection=db['metadata']
    data=collection.find_one({'link':url},{'S_no':1})
    sub_li=list(enumerate(sig[data['S_no']-1]))
    li=sorted(sub_li, key = lambda x: x[1],reverse=True) 
    index=[]
    for i in range(1,10,1):
        index.append(li[i][0])

    Recommended=[]
    for i in index:
        x=collection.find_one({'S_no':i+1})
        Recommended.append(x['link'])
        
    try:
        x=Recommend.objects.get(liked_by=user_id)
    except:

        #jarray=json.dumps(Recommended)
        Recommend.objects.create(liked_by=user,jsondata={'Recommended_articles':Recommended})
    else:
        x=Recommend.objects.get(liked_by=user_id)
        if x.jsondata is not None:
            for i in x.jsondata['Recommended_articles']:
                Recommended.append(i)
            #jarray=json.dumps(Recommended)
            Recommended=list(set(Recommended))
            x.jsondata['Recommended_articles']=Recommended
            x.save()

    db=client['scrapping']
    collection=db['metadata']
    data=collection.find_one({'link':url},{'title':1})
    title=data['title']
    
    return str(title)

