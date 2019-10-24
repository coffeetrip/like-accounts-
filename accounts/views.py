from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)


def follow(request, id):
    you = get_object_or_404(User, id=id)  # 팔로우할 사람
    me = request.user  # 나

    if me != you:   # 내가 나자신을 팔로우 못하게
        if me in you.followers.all():   # 내가 이미 팔로우 했니
            you.followers.remove(me)
        else:
            you.followers.add(me)
            # me.followings.add(you)

    return redirect('accounts:  user_page', id)


def delete(request, id):
    user_info = get_object_or_404(User, id)
    user = request.user

    if user_info == user:
        user_info.delete()  # 소셜과 모두 탈퇴
    return redirect('posts:ind  ex')


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def password(request):
    if request.method == 'POST':
        # password update (로그인한사람, 최신정보)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # 로그인
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def profile(request):
    user_info = request.user
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)
