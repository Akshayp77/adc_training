
from rest_framework.authtoken.models import Token
from .models import Recommend
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from django.http import JsonResponse
from .app_helper_func import recommendation
from .app_helper_func.getuser import get_user


# Create your views here.

def index(request):
    return HttpResponse("Welcome to home page")



class user_auth_api(APIView):
    ''''This Api is used to register a user and store information like first_name,last_name,username,
        password of a user in database.
    '''

    authentication_classes = [BasicAuthentication]
    
    def post(self,request):
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
    ''' This Api used for login if username and password are passed  is valid
    '''
    authentication_classes = [TokenAuthentication]
   
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            token=Token.objects.get(user=user)
            return HttpResponse(token,"Login Successfully")
        else:
            return HttpResponse("Password or username is wrong.Try again")

class liked_article(APIView):
    '''this Api takes url which is liked by user and return title of that url,it uses rec function from app_helper_fun
    '''
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        
        url = request.POST['url']
        user_id = get_user(request.auth.key)
        user = User.objects.get(id=user_id)
        title = recommendation.rec(url,user_id,user)
        return HttpResponse("Hello "+str(user).capitalize()+", You like this article  : "+title)



class recommended_articles(APIView):
    ''' this Api return all recommended articles related with particular user
    '''
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        
        user_id=get_user(request.auth.key)
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
    


