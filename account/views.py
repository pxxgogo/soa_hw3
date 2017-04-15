__author__ = 'pxxgogo'

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    return render(request, "index.html", {})


def login(request):
    if not request.user.is_authenticated():
        return render(request, "login.html", {})
    else:
        return HttpResponseRedirect("/")


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def register(request):
    return render(request, "register.html", {})


def finish_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        users_list = User.objects.filter(username=username)
        if len(users_list) > 0:
            user = users_list[0]
            user.email = email
            user.save()
            auth.login(request, user)
            return HttpResponseRedirect("/")
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return HttpResponseRedirect("/login")
    else:
        return render(request, "register.html", {})


def finish_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"error_info": "Fail to login the account."})
