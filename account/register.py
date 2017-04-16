from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from faceBook.faceApi import FaceAPI
from models import AccountUser


def register(request):
    if request.method == 'POST':
        print(request.FILES)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        users_list = AccountUser.objects.filter(username=username)
        if len(users_list) > 0:
            print("Username has existed")
            return render(request, "register.html", {"error_info": "Username has existed"})
        user = AccountUser()
        user.username = username
        user.password = make_password(password, None, 'pbkdf2_sha256')
        user.email = email
        try:
            user.portrait = request.FILES['file']
        except:
            print("Portrait goes wrong")
            return render(request, "register.html", {"error_info": "Portrait goes wrong"})
        try:
            person_id = FaceAPI.create_person(username)
        except:
            print("please retry later!")
            return render(request, "register.html", {"error_info": "please retry later!"})
        user.person_id = str(person_id)
        user.save()
        return HttpResponseRedirect("/login")
    else:
        return render(request, "register.html", {})
