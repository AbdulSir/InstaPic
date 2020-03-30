from django import forms
from django.contrib.auth import authenticate
from django.db.models import F
from instapic.models import User, Photo
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
  
class AjaxLogin(Ajax):

	def validate(self): #function that allows us to validate the login
		try:
			self.password = self.args[0]["password"]  
			self.email = self.args[0]["email"]
		except Exception as e:                                            #if no email and no password then thtrow exception
			return None, self.error("Malformed request, did not process.")

		#chech if the characters and their number is valid, if not then return appropriate error meassages
		if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.email): 
			return None, self.error("Invalid email syntax.")
		if len(self.password) < 6 or len(self.password) > 32:
			return None, self.error("Password must be between 6 and 32 characters long.")
		if len(self.email) < 6 or len(self.email) > 140:
			return None, self.error("Email must be between 6 and 32 characters long.")
		
		#check if email is in database
		if not User.objects.filter(email=self.email).exists():
			return None, self.error("Email or password is incorrect.")
		
		#check if password is in database by using the email to find the appropriate password
		if not check_password(self.password, User.objects.filter(email=self.email)[0].password):
			return None, self.error("Email or password is incorrect.")

		u = User.objects.filter(email=self.email)[0] #extract appropriate user from the database

		return u, self.success("User logged in!")  #return user with message


class AjaxSavePhoto(Ajax):

	def validate(self):  #function that validates the saving of a photo
		try:
			self.url = self.args[0]["url"]
			self.baseurl = self.args[0]["baseurl"]
			self.caption = self.args[0]["caption"]
		except Exception as e:               #if photo has no urls and no caption then throw exception
			return self.error("Malformed request, did not process.")

		if self.user == "NL":          #check if request came from logged in user
			return self.error("Unauthorised request.")

		if len(self.caption) > 140:    #check length of caption
				return self.error("Caption must be 140 characters.")

		#check that url of photo begins with uploadcare source so that outsiders can't upload		
		if self.url[0:20] != "https://ucarecdn.com" or self.baseurl[0:20] != "https://ucarecdn.com":
			return self.error("Invalid image URL")

		#uploadcare code, give back image colors
		result = urlopen(self.baseurl+"-/preview/-/main_colors/3/")
		data = result.read()
		data = json.loads(data.decode('utf-8'))

		main_colour = ""
		if data["main_colors"] != []:
			#main_colour = data["main_colors"][randint(0, 2)]
			for colour in data["main_colors"][randint(0, 2)]:
				main_colour = main_colour + str(colour) + ","
			main_colour = main_colour[:-1]

		
		p = Photo(url=self.url, baseurl=self.baseurl, owner=self.user.username, likes=0, caption=self.caption, main_colour=main_colour)
		p.save() 


		return self.success("Image Uploaded")
	
class AjaxPhotoFeed(Ajax):
	def validate(self):

		try:
			self.start = self.args[0]["start"]
		except Exception as e:
			return self.error("Malformed request, did not process.")

		out = []  #list of out
		followerslist = [self.user.username]  #list of followers
		profilepics = {}  #dictionary of profile pics

#---------------------------
		for follower in Followers.objects.filter(follower=self.user.username): #loop through all the followers of user  
			followerslist.append(follower.user)				#input followers into array
#---------------------------

#---------------------------
		for user in User.objects.filter(username__in=followerslist):   #loop through all users that are in follower list
			profilepics[user.username] = user.profilepic	       #for that user in the dictionary add that user profile pic
			if user.profilepic == "":     #if the users profile pic is empty 
				profilepics[user.username] = "static/assets/img/default.png"  #then use default
#---------------------------

#---------------------------
		for item in Photo.objects.filter(owner__in=followerslist).order_by('-date_uploaded')[int(self.start):int(self.start)+3]:  #loop through all the photos that have owner in follower list in order of their uploaded date
			if PhotoLikes.objects.filter(liker=self.user.username).filter(postid=item.id).exists():  #if a photo like done by the user for that  photo exists
				liked = True #set variable liked to true
			else:
				liked = False  #set variable liked to false

			out.append({ "PostID": item.id, "URL": item.url, "Caption": item.caption, "Owner": item.owner, "Likes": item.likes, "DateUploaded": item.date_uploaded.strftime("%Y-%m-%d %H:%M:%S"), "Liked": liked, "ProfilePic": profilepics[item.owner]+"", "MainColour": item.main_colour }) #append to out list the photos attributes as well as the owner profile pic
#---------------------------

		return self.items(json.dumps(out))

