from pymongo import MongoClient
PORT='27017'
client=MongoClient("mongodb://localhost:"+PORT+"/")
DB='scrapping'
DES_COLLECTION='discription'

META_COLLECTION='metadata'