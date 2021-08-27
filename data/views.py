from django import http
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import auth
from .data_helper_func import scrap,token



class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class scrap(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            scrap.scrap_metadata()
            return HttpResponse("DATA stored in database Successfully")
        else:
            return HttpResponse("Username or Password is incorrect")

class discription(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        scrap.scrap_description()
        token.remove_stopwords()
        token.steming_data()
        return HttpResponse("Data converted into tokens(removed stopwords,steming) and stored in database Successfully")


