from django import forms
from django.contrib.auth import authenticate
from django.db.models import F
from instapic.models import User
from django.contrib.auth.hashers import make_password, check_password
from urllib.request import urlopen
from random import randint

import json, re

class Ajax(forms.Form):

    args = []
    user = []

    #constructor
    def __init__(self, *args, **kwargs):
        self.args = args      #get the arguments and store them
        if len(args) > 1:     # if there is more than the data and post request
            self.user = args[1]  #user details
            if self.user.id == None: #if user is not logeed in
                self.user = "NL" #then he is anonymous

    def error(self, message):
        return json.dumps({ "Status": "Error", "Message": message }, ensure_ascii=False)

    def success(self, message):
        return json.dumps({ "Status": "Success", "Message": message }, ensure_ascii=False)
    
    #when request is succesful; send json out of database
    def items(self, json):
        return json

    def output(self):
        return self.validate() #do appropriate validation depending if its signup or login instance

class AjaxSignUp(Ajax):

    def validate(self):  #used to validate the sign-up
        try:
            self.username = self.args[0]["username"]
            self.password = self.args[0]["password"]
            self.email = self.args[0]["email"]
        except Exception as e:
            return self.error("Malformed request, did not process.") #if a user doesn't have either of the three things above, then throw exception


        if not re.match('^[a-zA-Z0-9_]+$', self.username):   #check if username contain valid charachters
        	return self.error("Invalid username, must be fit [a-zA-Z0-9_]")
        if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.email):  #check if email contain valid charachters
        	return self.error("Invalid email syntax.")
        if len(self.username) < 4 or len(self.username) > 20:  #check if username has enough characters
        	return self.error("Username must be between 3 and 20 characters long.")
        if len(self.password) < 6 or len(self.password) > 32:  #check if password has enough characters
        	return self.error("Password must be between 6 and 32 characters long.")
        if len(self.email) < 6 or len(self.email) > 140:      #check if email has enough characters
        	return self.error("Email must be between 6 and 32 characters long.")

        if User.objects.filter(username=self.username).exists():  #check if username already in use
        	return self.error("Username already in use.")

        if User.objects.filter(email=self.email).exists():       #check if email already in use
        	return self.error("Email address already in use.")

        u = User(username=self.username, password=make_password(self.password), email=self.email)  #create the user with the appropriate data (password is hashed using a django function)
        u.save()  #store user in the database

        return self.success("Account Created!")  #call the success function with the message input




