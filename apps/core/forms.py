from django import forms

from apps.core.models import Comment,Post


class CommentModelForm(forms.ModelForm):
    message = forms.CharField(label ="", widget = forms.TextInput (attrs ={
            'placeholder':'Add comment',
            'class': "shadow-none rounded-pill comment-input m-2",
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
        
class ThreadForm(forms.Form):
    username = forms.CharField(label ="", max_length=100)
    
class MessegeForm(forms.Form):
    message = forms.CharField(label ="", max_length=1000)