import json
from app.serializer import RecomendSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Recommend, create_auth_token
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


# Create your views here.

def index(request):
    return HttpResponse("Welcome to home page")

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class user_auth_api(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        if request.method=='POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            pass1=request.POST['password1']
            pass2=request.POST['password2']
            if pass1 !=pass2:
                return HttpResponse("password not matched")
            if User.objects.filter(username=username).exists():
                return HttpResponse("User already exist")
            else:
                user=User.objects.create_user(username=username,password=pass1,first_name=first_name,last_name=last_name)
                user.save()
                return HttpResponse("Hello "+username.capitalize()+",you are successfully registered")
class login(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        if request.method =='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                token=Token.objects.get(user=user)
                return HttpResponse(token,"Login Successfully")
            else:
                return HttpResponse("Password or username is wrong.Try again")

class Recommended_articles(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):

        url=request.POST['url']
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        
        db=client['scrapping']
        collection=db['discription']
        data1=collection.find({})
        l=[]
        for i in data1:
            l.append(" ".join(i['para']))
        vectorize = TfidfVectorizer()
        response = vectorize.fit_transform(l)
        #print(response.shape)
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
        
        return HttpResponse("Hello "+str(user).capitalize()+", You like this article  : "+str(data['title']))
        
    def get(self,request):
        
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        #x=Recommend.objects.get(liked_by=user_id)
        try:
            x=Recommend.objects.get(liked_by=user_id)
        except:
            return HttpResponse("You haven't like any article")
            
        else:
            x=Recommend.objects.get(liked_by=user_id)
            if x.jsondata is None:
                return HttpResponse("You haven't like any article")
            else:
                return JsonResponse(x.jsondata['Recommended_articles'],safe=False)
    

