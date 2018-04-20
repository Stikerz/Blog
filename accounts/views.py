from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate,login,logout

from .forms import LoginForm, RegisterForm, ProfileForm

# Create your views here.

def login_view(request):
    if  request.user.is_authenticated:
        return redirect('/articles/article_list/')
    else:
        form = LoginForm(request.POST or None)
        template = "login.html"
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/articles/article_list/')

        context = {'user_form': form}
        return render(request, template, context)

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if  request.user.is_authenticated:
        return redirect('/articles/article_list/')
    else:
        template = "register.html"
        user_form = RegisterForm(request.POST or None)
        profile_form = ProfileForm(request.POST or None)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password")
            new_user.set_password(password)
            new_user.save()
            profile = profile_form.save(commit=False)
            user = authenticate(username=new_user.username, password=password)
            profile.set_user(user)
            profile.save()
            login(request, user)
            return redirect('/articles/article_list/')

    context = {'register_form': user_form, 'profile_form':profile_form}
    return render(request, template, context)