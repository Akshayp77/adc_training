from app.app_helper_func.constant import META_COLLECTION, client, DB, DES_COLLECTION
from django.http.response import HttpResponse
from app.models import Recommend
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


def rec(url,user_id,user):
    '''this function finds tf-idf values using TFidfvectorizer class and find list  that using sigmoid_kernel and store 
       recommended articles in database and returns title of liked article 
    '''

    try:
        client
    except:
        return HttpResponse("Database is not connected")
    else:
        db=client[DB]
        collection=db[DES_COLLECTION]
        description_data=collection.find({})
        list_of_paras=[]
        for para in description_data:
            list_of_paras.append(" ".join(para['para']))
        vectorize = TfidfVectorizer()
        response = vectorize.fit_transform(list_of_paras)
        sig=sigmoid_kernel(response,response)
        db=client[DB]
        collection=db[META_COLLECTION]
        meta_data=collection.find_one({'link':url},{'S_no':1})
        sub_li=list(enumerate(sig[meta_data['S_no']-1]))
        li=sorted(sub_li, key = lambda x: x[1],reverse=True) 
        index=[]
        for i in range(1,10,1):
            index.append(li[i][0])
    
        recommended_list=[]
        for i in index:
            x=collection.find_one({'S_no':i+1})
            recommended_list.append(x['link'])
            
        try:
            x=Recommend.objects.get(liked_by=user_id)
            if x.jsondata is not None:
                for articles in x.jsondata['Recommended_articles']:
                    recommended_list.append(articles)
                recommended_list=list(set(recommended_list))
                x.jsondata['Recommended_articles']=recommended_list
                x.save()
        except:
            Recommend.objects.create(liked_by=user,jsondata={'Recommended_articles':recommended_list})
        
        collection=db[META_COLLECTION]
        data=collection.find_one({'link':url},{'title':1})
        title=data['title']
        return str(title)

