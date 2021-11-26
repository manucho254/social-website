from django import forms
from .models import Comment,Post

class CommentModelForm(forms.ModelForm):
    message = forms.CharField(label ="", widget = forms.TextInput (attrs ={
            'placeholder':'Add comment',
            'class': 'form-control comment-input  w-80 rounded-pill',
            'size': 75,
            "id": "message"
            }))
    class Meta:
        model = Comment
        fields = ["message"]
        
class PostModelForm(forms.ModelForm):
    body = forms.CharField(label ="", widget = forms.TextInput (attrs ={
        'placeholder':'Add post',
        'class': "post-body w-75",
        'rows': "3",
        "id": "body"
        }))
    class Meta:
        model = Post
        fields = ["caption", "body",]