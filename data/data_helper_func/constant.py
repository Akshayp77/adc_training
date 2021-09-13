from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")
DB='scrapping'
DES_COLLECTION='discription'
META_COLLECTION='metadata'
URL="https://news.ycombinator.com/"