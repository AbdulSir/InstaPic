from sqlite3.dbapi2 import Date

import pymongo
import dns
from pymongo import MongoClient

#Adds a user to the database
def add_user(name,password):
  new_User ={"_id": name,
        "password": password,
        "nontification": [],
        "followers": [],
        "followed": [],
        "checkedNontification": [],
        "NontificationCtr": 0}
  Users.insert_one(new_User)

#Check to see if login info is correct, if it is then it returns true and if not then it returns false
def login(name,password):
  temp_user = Users.find_one(name)
  if temp_user == None:
    return False
  if temp_user["password"] == password:
    return True
  return False

#Returns None (null) if there is no user in the database with that name
def search_user(name):
  temp_user = Users.find_one(name)
  if temp_user == None:
    return None
  return temp_user

#Checks to see if the photo and user exists, if they do it adds the comment and user name to the photo object
#Allows for the same comment and user to be added to the array
def comment(photo,name,comment):
  temp_user = Users.find_one(name)
  if temp_user == None:
    return None
  temp_photo = Photos.find_one(photo)
  if temp_photo == None:
    return None
  Photos.update_one({'_id':photo},{'$push' :{"comments.usernames" : name}})
  Photos.update_one({'_id':photo},{'$push' :{"comments.comment" : comment}})
  
#Makes the user follow the other account and adds them to the followed array
def follow_user(name_to_follow,user):
  temp_user = Users.find_one(user)
  if temp_user == None:
    return None
  temp_name_to_follow = Users.find_one(name_to_follow)
  if temp_name_to_follow == None:
    return None
  Users.update_one({'_id':name_to_follow},{'$addToSet' :{"followers" : user}})
  Users.update_one({'_id':user},{'$addToSet' :{"followed" : name_to_follow}})

#Allows a user to like a photo
def like_photo(photo,name):
  temp_photo = Photos.find_one(photo)
  if temp_photo == None:
    return False
  temp_user = Users.find_one(name)
  if temp_user == None:
    return False
  #Checks to see if the user has liked the photo before or not
  check_if_liked = Photos.find_one({'_id':photo,"likes" : name})
  if check_if_liked == None:
    Photos.update_one({'_id':photo},{'$addToSet' :{"likes" : name}})
    Photos.update_one({'_id':photo},{'$inc' :{"likesCtr": 1}})


cluster = MongoClient("mongodb+srv://abdul:1234@instapic-ya3mh.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["InstaPic"]
Users = db["Users"]
Photos = db["Photos"]

#Test add user
#add_user("Tyler","Password")

#Test login
#print(login("Tyler","Password"))

#Test comment
#comment("testPhoto","Tyler","test comment")

#Test follow
#follow_user("Tyler", "Elie")

#Test Like photo
#like_photo("testPhoto","Tyler")
