from django import forms
from .models import Comment

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