from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ("male", "male"),
    ("female", "female")
    )

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',  on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    birthday = models.DateField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES, default = 'Enter Gender')
    profile_image = models.ImageField(upload_to="profile/",  null=True, blank=True)
    profile_created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.username)
