from django.db import models


class Users(models.Model):
    pass

class Profile(models.Model):
    username = models.CharField(max_length=40)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to="images",  null=True, blank=True)
    
    def __str__(self):
        return "{}".format(self.username)
