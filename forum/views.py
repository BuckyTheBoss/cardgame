from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'post_list': posts})


def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'view_post.html', {'post': post})

@login_required
def create_post(request):

    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')
        p = Post.objects.create(profile=request.user.profile, title=title, content=content)
        return redirect('view_post', p.id)
    return render(request, 'create_post.html')

@login_required
def new_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = request.user.profile
            comment.post = post
            comment.save()
            return redirect('view_post', comment.post.id)
        return redirect('index')
    form = CommentForm()

    return render(request, 'new_comment.html', {'form': form, 'btn_text': 'Add'})

@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()

        return redirect('index')
    form = CommentForm(instance=comment)

    return render(request, 'new_comment.html', {'form': form,'btn_text': 'Save'})
