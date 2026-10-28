from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Profile, Post, Comment, Follow

def get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile

def feed(request):
    posts = Post.objects.select_related("author").prefetch_related(
        "likes", "comments__author"
    ).order_by("-created")
    return render(request, "feed.html", {"posts": posts})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect("feed")
    return render(request, "form.html", {"form": form, "heading": "Create account"})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("feed")

@login_required
@require_POST
def create_post(request):
    content = request.POST.get("content", "").strip()
    if content:
        Post.objects.create(author=request.user, content=content[:1000])
    return redirect("feed")

@login_required
@require_POST
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.POST.get("next", "feed"))

@login_required
@require_POST
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get("content", "").strip()
    if content:
        Comment.objects.create(
            post=post, author=request.user, content=content[:500]
        )
    return redirect(request.POST.get("next", "feed"))

def profile(request, username):
    person = get_object_or_404(User, username=username)
    get_profile(person)
    posts = person.posts.prefetch_related("likes", "comments__author").order_by("-created")
    is_following = request.user.is_authenticated and Follow.objects.filter(
        follower=request.user, following=person
    ).exists()
    return render(request, "profile.html", {
        "person": person,
        "posts": posts,
        "is_following": is_following,
        "followers_count": person.followers.count(),
        "following_count": person.following.count(),
    })

@login_required
def bio(request):
    profile = get_profile(request.user)
    if request.method == "POST":
        profile.bio = request.POST.get("bio", "").strip()[:250]
        profile.save()
        return redirect("profile", username=request.user.username)
    return render(request, "bio.html", {"profile": profile})

@login_required
@require_POST
def follow(request, username):
    person = get_object_or_404(User, username=username)
    if person != request.user:
        link, created = Follow.objects.get_or_create(
            follower=request.user, following=person
        )
        if not created:
            link.delete()
    return redirect("profile", username=person.username)
