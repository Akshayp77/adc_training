#from data.views import description
from data.data_helper_func.constant import client, DB, DES_COLLECTION
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def remove_stopwords():
    '''This function remove stopwords using nltk library function "stopwords" and converted data into token
    '''
    try:
        client
    except:
        return 0
    else:
        db=client[DB]
        collection=db[DES_COLLECTION]
        description_collection=collection.find({})
        words = list(stopwords.words('english'))
        add_list=['.',',',';',':',"/",')','(','[',']','{','}','-','#','"',"'",'’','?','@','!',"''",'``','``','“','”']
        words=words+add_list
        for description_data in description_collection:
            
            try:
                #if description_data['para'] does not have any paragraph
                word_tokens=word_tokenize(description_data['para'])
            except:
                continue
            else:
                imp_words=[]
                for j in word_tokens:
                    if j.lower() not in words:
                        imp_words.append(j)
            collection.update_one({"para":description_data['para']},{"$set":{"para": imp_words }})
        return 1

def steming_data(request):
    '''this function uses nltk library class portStemmr for steming
       ex- converted "Liked","Likes" into "Like" 
    '''
    
    try:
        client
    except:
        return 0
    else:
        db=client[DB]
        collection=db[DES_COLLECTION]
        description_collection=collection.find({})
        ps=PorterStemmer()
        for description_data in description_collection:
            stemed_data=[]
            for j in range(len(description_data['para'])):
                stemed_data.append(ps.stem(description_data['para'][j]))
            collection.update_one({"para":description_data['para']},{"$set":{"para": stemed_data}})
        return 1
