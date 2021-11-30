from django import forms
from .models import Comment,Post

class CommentModelForm(forms.ModelForm):
    message = forms.CharField(label ="", widget = forms.TextInput (attrs ={
            'placeholder':'Add comment',
            'class': "shadow-none rounded-pill comment-input",
            'rows': "3",
            "id": "message"
            }))
    class Meta:
        model = Comment
        fields = ["message"]
        
class PostModelForm(forms.ModelForm):
    caption = forms.CharField(label ="", widget = forms.TextInput (attrs ={
        'placeholder':'Add Caption',
        'class': "shadow-none  mb-2 mt-4",
        'rows': "3",
        "id": "caption"
        }))
    body = forms.CharField(label ="", widget = forms.TextInput (attrs ={
        'placeholder':'Post body',
        'class': "shadow-none post-body mb-2 mt-4",
        'rows': "3",
        "id": "body"
        }))
    
    class Meta:
        model = Post
        fields = ["caption", "body", "post_image"]