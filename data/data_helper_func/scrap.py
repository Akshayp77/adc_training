from django.shortcuts import render
from re import T, findall
import requests
from bs4 import BeautifulSoup
import pymongo

def scrap_metadata():
    url="https://news.ycombinator.com/"
    r=requests.get(url)
    htmlContent=r.content
    sp=BeautifulSoup(htmlContent,'html.parser')
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    more=''  
    while more!=None:
        url="https://news.ycombinator.com/"
        if more!='':
            url=url+more['href']
        r=requests.get(url)
        htmlContent=r.content
        sp=BeautifulSoup(htmlContent,'html.parser')
        t=sp.find_all('td',class_='subtext')
        for j in t:
            n= j.find_all_next()
            t1=j.findParent()
            if j.find('span',class_='score') not in n:
                e=t1.find_all_previous('span',class_='rank')
                num=e[0].text
                flag1=1
                if len(num)==3:
                    num=int(num[0:2:])
                else:
                    num=int(num[0:1:])
        lnk=sp.find_all('a',class_='storylink',href=True,text=False)
        site=sp.find_all('span',class_='sitestr')
        s_no=sp.find_all('span',class_='rank')
        by=sp.find_all('a',class_="hnuser")
        title=sp.find_all('a',class_='storylink')
        points=sp.find_all('span',class_="score")
        time=sp.find_all('span',class_="age")
        l=[]
        c={}
        if flag1==1:
            points.insert(num-1,'0 points')
            by.insert(num-1,'')
        else:
            num=-1

        for i in range(len(s_no)):
            c={}
            n=s_no[i].text
            n=n[0:len(n)-1]
            c['S_no']=int(n)
            chk=""
            chk=title[i].text
            if chk in title:
                continue
            c['title']=title[i].text
            if 'item?id=' in lnk[i]['href']:
                c['link']='https://news.ycombinator.com/'+lnk[i]['href']
            else:
                c['link']=lnk[i]['href']
            if '.PDF' in c['link']:
                print(c['link'])
            if i==num-1:
                c['points']='0 points'
                c["by"]=''
            else:
                c['points']=points[i].text
                c['by']=by[i].text
            c['time']=time[i].text
            
            db=client['scrapping']
            collection=db['metadata']
            collection.insert_one(c)
            l=collection.find_one({"S_no":int(n)})
            #print(l)
            new_d={}
            new_d['p_id']=l['_id']
            new_d['link']=l['link']
            collection=db['discription']
            collection.insert_one(new_d)
            
            
        more=sp.find('a',class_='morelink',href=True,text=False)

def scrap_description():
    
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['scrapping']
    collection=db['discription']
    
    dt=collection.find({})
    for i in dt:
        p,q,r1=" ",[],[]
        url=i['link']
        if url=="https://www.sacbee.com/news/politics-government/capitol-alert/article253647838.html":
            continue
        if ".pdf"in i['link'] or ".PDF"in i['link']  or ".Pdf"in i['link'] or "https://www.seattletimes.com" in url:
            continue
        try:        
            r=requests.get(url)
        except:
            db.discription.update_one({"_id":i['_id']},{"$set": {'para':p,'img':q,'urls':r1}}) 
            continue
    
        else:
            htmlContent=r.content
            sp=BeautifulSoup(htmlContent,'html.parser')
        try:
            img=sp.find_all('img',src=True)
        except:
            img=[]
        else:
            for j in img:
                if 'https' not in j['src']:
                    pass
                else:
                    q.append(j['src'])

        try:
            para=sp.find_all('p')
        except:
            p=" "
        else:
            for j in para:
                p=p+j.text

        try:
            urls=sp.find_all('a',href=True,text=False)
        except:
            urls=[]
        else:
            for k in urls:
                r1.append(k['href'])
        db.discription.update_one({"_id":i['_id']},{"$set": {'para':p,'img':q,'urls':r1}})