from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import  BasicAuthentication
from .data_helper_func.token import remove_stopwords,steming_data
from .data_helper_func.scrap import scrap_description,scrap_metadata



class scrap(APIView):
    '''this API is used to scrap meta information using scrap function present in data_helper_fun directory
       and store scrapped data in database.
    '''
    authentication_classes = [BasicAuthentication]
    def post(self,request):
        output=scrap_metadata()
        if output==0:
            return HttpResponse("Database is not connected")
        return HttpResponse("DATA stored in database Successfully")


class description(APIView):
    '''this API is used to scrap description of meta information using description function present in data_helper_fun 
        directory and store scrapped data in database.
    '''
    authentication_classes =[BasicAuthentication]
    def post(self,request):
        output1=scrap_description()
        output2=remove_stopwords()
        output3=steming_data()
        if output1*output2*output3==0:
            return HttpResponse("database is not connected")
        return HttpResponse("Data converted into tokens(removed stopwords,steming) and stored in database Successfully")


