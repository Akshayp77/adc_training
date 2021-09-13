from re import T
import requests
from bs4 import BeautifulSoup
from data.data_helper_func.constant import client,DB,URL,DES_COLLECTION,META_COLLECTION

def scrap_metadata():
    ''' This function scrap meta information of site using beautifulsoup and store scrapped data in database
    '''

    url=URL
    req=requests.get(url)
    htmlContent=req.content
    sp=BeautifulSoup(htmlContent,'html.parser')
    try:
        client
    except:
        return 0
    else:
        next_page_url=''  
        while next_page_url!=None:
            url=URL
            if next_page_url!='':
                url=url+next_page_url['href']
            req=requests.get(url)
            htmlContent=req.content
            sp=BeautifulSoup(htmlContent,'html.parser')
            td_tag=sp.find_all('td',class_='subtext')
            for j in td_tag:
                next_tag= j.find_all_next()
                parent_tag=j.findParent()
                if j.find('span',class_='score') not in next_tag:
                    prev_tag=parent_tag.find_all_previous('span',class_='rank')
                    num=prev_tag[0].text
                    flag1=1
                    if len(num)==3:
                        num=int(num[0:2:])
                    else:
                        num=int(num[0:1:])
            lnk=sp.find_all('a',class_='storylink',href=True,text=False)
            s_no=sp.find_all('span',class_='rank')
            by=sp.find_all('a',class_="hnuser")
            title=sp.find_all('a',class_='storylink')
            points=sp.find_all('span',class_="score")
            time=sp.find_all('span',class_="age")
            l=[]
            meta_data={}
            if flag1==1:
                points.insert(num-1,'0 points')
                by.insert(num-1,'')
            else:
                num=-1

            for i in range(len(s_no)):
                meta_data={}
                n=s_no[i].text
                n=n[0:len(n)-1]
                meta_data['S_no']=int(n)
                meta_data['title']=title[i].text
                if 'item?id=' in lnk[i]['href']:
                    meta_data['link']=URL+lnk[i]['href']
                else:
                    meta_data['link']=lnk[i]['href']
                if i==num-1:
                    meta_data['points']='0 points'
                    meta_data["by"]=''
                else:
                    meta_data['points']=points[i].text
                    meta_data['by']=by[i].text
                meta_data['time']=time[i].text
                
                db=client[DB]
                collection=db[META_COLLECTION]
                collection.insert_one(meta_data)
                l=collection.find_one({"S_no":int(n)})
                description_data={}
                description_data['p_id']=l['_id']
                description_data['link']=l['link']
                collection=db[DES_COLLECTION]
                collection.insert_one(description_data)
                
                
            next_page_url=sp.find('a',class_='morelink',href=True,text=False)
        return 1

def scrap_description():
    ''' This function scrap description of meta information using beautifulsoup and store data in database.
    '''
    try:
        client
    except:
        return 0
    else:
        db=client[DB]
        collection=db[DES_COLLECTION]
        
        description_collection=collection.find({})
        for description_data in description_collection:
            para_str,img_list,url_list=" ",[],[]
            url=description_data['link']
            if ".pdf" in description_data['link'] or ".PDF" in description_data['link']  or ".Pdf" in description_data['link'] in url:
                continue
            try:        
                req=requests.get(url)
            except:
                collection.update_one({"_id":description_data['_id']},{"$set": {'para':para_str,'img':img_list,'urls':url_list}}) 
                continue
        
            else:
                htmlContent=req.content
                sp=BeautifulSoup(htmlContent,'html.parser')
            try:
                img_data=sp.find_all('img',src=True)
            except:
                img_list=[]
            else:
                for imgs in img_data:
                    if 'https' not in imgs['src']:
                        pass
                    else:
                        img_list.append(imgs['src'])

            try:
                para_data=sp.find_all('p')
            except:
                para_str=" "
            else:
                for p in para_data:
                    para_str=para_str+p.text

            try:
                urls_data=sp.find_all('a',href=True,text=False)
            except:
                url_list=[]
            else:
                for urls in urls_data:
                    url_list.append(urls['href'])
            collection.update_one({"_id":description_data['_id']},{"$set": {'para':para_str,'img':img_list,'urls':url_list}})
    return 1