from cProfile import Profile

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm1, RegisterForm2, LoginForm
from auth_app.models import UserProfile


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm1(request.POST)
        form2 = RegisterForm2(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            UserProfile.objects.create(
                user=user,
                bio=form2.cleaned_data['bio'],
                occupation=form2.cleaned_data['occupation'],
                profile_image=form2.cleaned_data['profile_image'],
                website=form2.cleaned_data['website']
            )

            login(request, user)
            return redirect('/')


        return render(request, "auth_app/register.html", {'form': form, 'form2': form2})

    else:
        form = RegisterForm1()
        form2 = RegisterForm2()

    return render(request, "auth_app/register.html", {'form': form, 'form2': form2})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
