import tweepy,csv
import pymongo
import unicodedata
import string
all_letters = string.ascii_letters +string.digits+'"'+string.ascii_uppercase+" -.,"
n_letters = len(all_letters)

def unicodeToAscii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn' and c in all_letters)


USERNAME='manos'
PASSWORD='11Ian19891989'
HOST='d0002332'
PORT='27017'
MONGO_DATABASE='large_papers'
count=1
client = pymongo.MongoClient('mongodb://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+MONGO_DATABASE)
db = client['twitter']

def get_profile_info(prof_id):
	profile_info=API.get_user(prof_id)
	Name=unicodeToAscii(profile_info._json['name'])
	location=unicodeToAscii(profile_info._json['location'])
	profile_location=profile_info._json['profile_location']
	profile_id=profile_info._json['id_str']
	followers=profile_info._json['followers_count']
	followings=profile_info._json['friends_count']
	tweets=profile_info._json['statuses_count']
	if len(location)>1 and len(Name.split(' '))>=2:
		dict_write={'id':profile_id,'name':Name,'location':location,'followers':followers,'followings':followings,'status_number':tweets}
		results=db['users'].insert_one(dict_write)

text=open('names.txt','rb')
names=[line.strip() for line in text]
text.close()


token='413525218-K44QPskEZpu4fPX1aR2fwzgIVwEwxmyopzV0tbBj'
TokenSecret='1ItrLvOs7n4RkB03qYOlKgsW7yjPAjNCM5u92i1v6TnwB'
ConsKey='zA4oYWaaVX4QwHbpo1vD28vJk'
ConsSecret='VHxuTJKFAwtpeOktYxHy4XgS9TXjbqq3jEgk3ii6lrwXzIAMkh'

auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
auth.set_access_token(token, TokenSecret)
API = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

for n in names:
	followers=API.followers(n)
	for f in followers:
		prof_id=f._json['id_str']
		try:
			get_profile_info(prof_id)
		except:
			pass
