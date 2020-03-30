"""instapic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from views

from django.conf.urls import url
from django.urls import path

from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),    #homepage
    url(r'^sign-up$', views.signup), 
    url(r'^ajax-sign-up$', views.ajaxsignup),   #signup page
    url(r'^ajax-login$', views.ajaxlogin),      #login page
    url(r'^ajax-save-photo$', views.ajaxsavephoto),
    url(r'^ajax-photo-feed$', views.ajaxphotofeed),  #feed page
    url(r'^(?P<username>[a-zA-Z0-9_]+)$', views.profile),  #profile page
    url(r'^ajax-profile-feed$', views.ajaxprofilefeed),
    url(r'^ajax-set-profile-pic$', views.ajaxsetprofilepic),
    url(r'^ajax-like-photo$', views.ajaxlikephoto),
    url(r'^ajax-follow$', views.ajaxfollow),
    
    url(r'ajax-post_comment$', views.ajaxcomment),    #<<<<==============WORKING AREA
    url(r'^ajax-comment-post$', views.ajaxcommentpost),
    path('logout/', views.user_logout ,name="user_logout")  
    
]
