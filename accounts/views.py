from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, LoginForm, ProfileEditForm, SettingForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile, Setting
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from posts.models import *
from forum_app.models import Post as ForumPost


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return HttpResponse('Account disabled')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
            return render(request, 'registration/login.html', {'form':form})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            form = LoginForm()
            return render(request, 'registration/login.html', {'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = new_user.username.lower()
            try:
                new_user.save()
            except IntegrityError:
                messages.error(request, 'Name taken.')
                return render(request, 'registration/register.html', {'user_form': user_form})
            profile = Profile.objects.create(user=new_user, display_name=new_user.username)
            settings = Setting.objects.create(user=new_user)
            settings.ciphers.add(Cipher.objects.get(name="Simple"))
            settings.ciphers.add(Cipher.objects.get(name="English"))
            settings.ciphers.add(Cipher.objects.get(name="Jewish"))
            settings.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'registration/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def dashboard(request):
    try:
        Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        Profile.objects.create(user=request.user)
    return render(request, "dashboard.html")


@login_required
def edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'edit.html', {'form': form})


@login_required
def settings(request):
    user = request.user
    try:
        settings = Setting.objects.get(user=user)
    except ObjectDoesNotExist:
        settings = Setting.objects.create(user=user)
        settings.ciphers.add(Cipher.objects.get(name="Simple"))
        settings.ciphers.add(Cipher.objects.get(name="Jewish"))
        settings.save()
        print('made settings')
    if request.method == 'POST':
        form = SettingForm(instance=request.user.profile.settings, data=request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'settings.html', {'form': form})

        else:
            print("what")
            form = SettingForm(instance=request.user.profile.settings)
            return render(request, 'settings.html', {'form': form})
    else:
        print(user.profile.settings.ciphers)
        form = SettingForm(instance=request.user.profile.settings)
    return render(request, 'settings.html', {'form': form})


def profile_page(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by("-date")
    imgs = ForumPost.objects.filter(author=user).order_by("-created_at")
    return render(request, 'profile.html', {'profile': user.profile, 'posts': posts, 'imgs': imgs})