from django.db import models
#what goes into the database
class User(models.Model):
    is_authenticated = True
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=140)
    last_login = models.DateTimeField(auto_now=True)
    profilepic = models.CharField(max_length=255, default="")
