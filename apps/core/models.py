from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

from PIL import Image

from io import BytesIO


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="author")
    caption = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    post_slug = models.SlugField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True,  related_name="likes")
    comments = models.ManyToManyField("Comment", blank=True,  related_name="comments")
    post_image = models.ImageField(upload_to="uploads/post_images/", blank=True, null=True)
    post_thumbnail = models.ImageField(upload_to="uploads/post_images/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}  | {}".format(self.author, self.caption) 
    
    def get_post_image(self):
        if self.post_image:
            return 'http://127.0.0.1:8000' + self.post_image.url
        return ''
    
    def get_post_thumbnail(self):
        if self.post_thumbnail:
            return 'http://127.0.0.1:8000' + self.post_image.url
        else:
            if self.post_thumbnail:
                self.post_image = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.post_thumbnail.url
            else:
                return ''

    def make_thumbnail(self, post_image, size=(300, 200)):
        img = Image.open(post_image)
        img.convert('RGB')
        img.post_thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=post_image.caption,)

        return thumbnail
    
    def save(self, *args, **kwargs):
        self.post_slug = slugify(self.caption)
        super(Post, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ["-created_on"]

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    commented_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, blank=True,  related_name="comment_likes")
    parent = models.ForeignKey('self',  on_delete=models.CASCADE,  blank=True, null=True,  related_name="+")
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by("-commented_on").all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ["-commented_on"]
        
class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', related_name="+", on_delete=models.CASCADE, blank=True,  null=True)
    comment = models.ForeignKey('Comment', related_name="+", on_delete=models.CASCADE,  blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    
    def __str__(self):
        return "{} || {} ".format(self.to_user, self.from_user)
    
    class Meta:
        ordering = ["-date"]
    
class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    
class MessegeModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+',  on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    reciever_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    messege_image = models.ImageField(upload_to="uploads/message_images/", blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-date"]
        