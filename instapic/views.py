from django.shortcuts import render, redirect
from .models import User, Followers, Comment
from .forms import *
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse
from django.http import HttpResponseRedirect

#functions come from forms.py

#signing up using ajax
def ajaxsignup(request):
    ajax = AjaxSignUp(request.POST)  #create instance of signup and take post request
    context = {'ajax_output': ajax.output() } #store variables to be put into template
    return render(request, 'ajax.html', context) 

#logging in using ajax
def ajaxlogin(request):
	ajax = AjaxLogin(request.POST) #create instance of login and take post request
	logged_in_user, output = ajax.validate() #if validated, store output into variables
	if logged_in_user != None:  #if variable is not empty
	    login(request, logged_in_user) #use django method to login
	context = {'ajax_output': output} #store variables to be put into template
	return render(request, 'ajax.html', context)

#signing up
def signup(request):
    context = {}
    return render(request, 'sign-up.html', context)

#logging out
def user_logout(request):
	context={}
	logout(request)
	return redirect(home)

#------------------------------------------------------------------------
#------------------------------------------------------------------------WORKING AREA
#------------------------------------------------------------------------
#------------------------------------------------------------------------

#commenting
def ajaxcomment(request):
	ajax=AjaxComment(request.POST, request.user)
	context={'ajax.output': ajax.output()}
	return render(request, 'ajax.html', context)


#creating comment feed
def ajaxcommentpost(request):  
    ajax = AjaxCommentPost(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

#home page
def home(request):
	context = {}
	if request.user.is_authenticated: #check if user is logged in
		u = User.objects.filter(username=request.user.username)[0] #get user data from database
		if u.profilepic == "":   #check if there is a profile photo
			u.profilepic = "static/assets/img/default.png"  #if no profile photo then set to default
		context = { 'user': request.user, 'ProfilePic': u.profilepic }  #store info about user
		return render(request, 'logged-in-index.html', context)  #create a logged in page using the logged-in-index template

	return render(request, 'index.html', context) #if user is not logged in, return normal index page

#saving a photo
def ajaxsavephoto(request):
	ajax = AjaxSavePhoto(request.POST, request.user)
	context = { 'ajax_output': ajax.output() }
	return render(request, 'ajax.html', context)

#creating main feed
def ajaxphotofeed(request):  
    ajax = AjaxPhotoFeed(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

#creating profile feed
def ajaxprofilefeed(request):
	ajax = AjaxProfileFeed(request.GET, request.user)
	context = { 'ajax_output': ajax.output() }
	return render(request, 'ajax.html', context)

#creating a profile
def profile(request, username):
	if User.objects.filter(username=username).exists():
		u = User.objects.filter(username=username)[0]
		
		if not Followers.objects.filter(user=username, follower=request.user.username).exists():
			following = "Follow"
		else:
			following = "Unfollow"
		
		if u.profilepic == "":
			u.profilepic = "static/assets/img/default.png"
		context = { "ProfilePic": u.profilepic, "whosprofile": username, "logged_in_as": request.user.username, "following": following } 
		if request.user.is_authenticated:
			return render(request, 'logged-in-profile.html', context)
		return render(request, 'profile.html', context)
	else:
		return redirect(home)

#creating a profile picture
def ajaxsetprofilepic(request):
	ajax = AjaxSetProfilePic(request.POST, request.user)
	context = { 'ajax_output': ajax.output() }
	return render(request, 'ajax.html', context)

#liking a picture
def ajaxlikephoto(request):
	ajax = AjaxLikePhoto(request.GET, request.user)
	context = { 'ajax_output': ajax.output() }
	return render(request, 'ajax.html', context)

#follow a user
def ajaxfollow(request):
	ajax = AjaxFollow(request.GET, request.user)
	context = { 'ajax_output': ajax.output() }
	return render(request, 'ajax.html', context)
