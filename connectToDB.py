from sqlite3.dbapi2 import Date

import pymongo
import dns
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://abdul:1234@instapic-ya3mh.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["InstaPic"]
Users = db["Users"]
Photos = db["Photos"]

user1 ={"_id": "Abdul",
        "password": "123",
        "nontification": ['Elie Posted a new picture. ', 'Another nontification'],
        "followers": "Users _id (e.g Tyler)",
        "followed": "Users _id (e.g Elie)",
        "checkedNontification": "An array of strings",
        "NontificationCtr": 5}

Users.insert_one(user1)

Photo1 = {"image": ".jpg (extension)",
          "username": "Abdul (The person who posted the picture)",
          "time": "The time of which this picture was posted",
          "likes": ['Elie', 'Aresny', 'Adam', 'Rakimul','Tyler'],
          "likesCtr": 5,
          "comments": {"usernames": ['Elie', 'Adam'],
                       "comment": ['Nice picture', 'It looks good']}
          }

Photos.insert_one(Photo1)



