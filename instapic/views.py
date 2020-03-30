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

#signing up
def signup(request):
    context = {}
    return render(request, 'sign-up.html', context)

#logging in using ajax
def ajaxlogin(request):
	ajax = AjaxLogin(request.POST) #create instance of login and take post request
	logged_in_user, output = ajax.validate() #if validated, store output into variables
	if logged_in_user != None:  #if variable is not empty
	    login(request, logged_in_user) #use django method to login
	context = {'ajax_output': output} #store variables to be put into template
	return render(request, 'ajax.html', context)

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
