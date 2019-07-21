from django.shortcuts import render
from . import forms

from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
# Create your views here.

def index(request):
    return render(request, "fifth_app/index.html")

@login_required
def special(request):
    return HttpResponse("You are logged out in, Nice!")

@login_required#this view requires a person to be logged in to see this
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# def login(request):
#     return render(request, "fifth_app/login.html")

def register(request):
    registered  =False
    if request.method == "POST":
        user_form = forms.UserForm(data = request.POST)
        profile_form = forms.UserProfileInfoForm(data= request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    content_dict = {"user_form":user_form, "profile_form": profile_form, "registered":registered}
    return render(request, "fifth_app/register.html", content_dict)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid Login details supplied!")
    else:
        return render(request, "fifth_app/login.html")
