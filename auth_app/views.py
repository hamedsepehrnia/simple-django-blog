from cProfile import Profile

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from auth_app.models import UserProfile


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "username or password is incorrect")
            return redirect('login')

    return render(request, "auth_app/login.html")


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        bio =request.POST.get('bio')
        occupation = request.POST.get('occupation')
        profile_image = request.FILES.get('profile_image')
        website = request.POST.get('website')
        name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password1 != password2:
            messages.error(request, "passwords don't match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "username has already been taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "email has already been registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1, first_name=name, last_name=last_name)
        UserProfile.objects.create(user=user, bio=bio, occupation=occupation, profile_image=profile_image, website=website)
        login(request, user)
        return redirect('/')

    return render(request, "auth_app/register.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
