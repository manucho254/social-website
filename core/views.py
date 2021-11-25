from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.contrib import messages
from .forms import CommentModelForm
from django.http import JsonResponse
from django.core import serializers


def home_view(request):
    posts = Post.objects.all()
    if request.method == "POST":
        commentForm = CommentModelForm(request.POST or None)
        if commentForm.is_valid():
            commentForm.save()
            return redirect("home")
    else:
        commentForm = CommentModelForm()
    context = {
        "posts": posts,
        "commentForm": commentForm
    }
    return render(request,  "index.html",  context)


# def commentView(request):

#     # request should be ajax and method should be POST.

#     if request.is_ajax and request.method == "POST":

#         form = CommentModelForm(request.POST)

#         # save the data and after fetch the object in instance

#         if form.is_valid():

#             instance = form.save()

#             # serialize in new friend object in json

#             ser_instance = serializers.serialize('json', [ instance, ])

#             # send to client side.

#             return JsonResponse({"instance": ser_instance}, status=200)

#         else:

#             # some form errors occured.

#             return JsonResponse({"error": form.errors}, status=400)
        
#     return JsonResponse({"error": ""}, status=400)
