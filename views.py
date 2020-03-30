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
