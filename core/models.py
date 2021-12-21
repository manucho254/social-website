from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="author")
    caption = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    post_slug = models.SlugField(max_length=30, blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True,  related_name="likes")
    comments = models.ManyToManyField("Comment", blank=True,  related_name="comments")
    post_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    post_thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_on"]
    
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
        self.slug = slugify(self.caption)
        super(Post, self).save(*args, **kwargs)
  

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    commented_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ["-commented_on"]
