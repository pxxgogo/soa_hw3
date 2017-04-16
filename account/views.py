__author__ = 'pxxgogo'

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    return render(request, "index.html", {})


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

