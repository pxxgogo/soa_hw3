# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

def face_gallery_view(request):
    if not request.user.is_active:
        return HttpResponseRedirect("/")
    faces = []
    for face in request.user.face_book.all():
        faceInfo = {}
        faceInfo["face_url"] = face.face.url
        faceInfo["face_id"] = face.id
        faceInfo["age"] = face.age
        faceInfo["emotion"] = face.emotion
        faces.append(faceInfo)
    return render(request, "face_gallery.html",
                  {'faces_list': faces})

def add_face_view(request):
    return render(request, "add_face.html", {})
