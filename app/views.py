
from rest_framework.authtoken.models import Token
from .models import Recommend, create_auth_token
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django.http import JsonResponse
from .app_helper_func import recommendation


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
        x=recommendation.rec(url,user_id,user)

        return HttpResponse("Hello "+str(user).capitalize()+", You like this article  : "+x)
        
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
    

