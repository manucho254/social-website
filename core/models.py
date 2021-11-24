from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name="author")
    title = models.CharField(max_length=200,  blank=True, null=True)
    post_image = models.ImageField(upload_to="images")
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} posted {}".format(self.author, self.title) 

class Comment(models.Model):
    # message_by = models.ForeignKey(Profile,  on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    commented_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message_by
    
    class Meta:
        ordering = ["-commented_on"]
